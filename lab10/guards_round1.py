"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _valid_approval(ctx, approval_id: str | None, ticket_id: str, order_id: str, amount_vnd: int) -> bool:
    if not approval_id:
        return False
    rows = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not rows:
        return False
    a = rows[0]
    req_approver = (ctx.gates.get("operations") or {}).get("approver_id")
    if req_approver and a.get("approver_id") != req_approver:
        return False
    return (
        a.get("status") == "valid"
        and a.get("ticket_id") == ticket_id
        and a.get("order_id") == order_id
        and bool(a.get("expires_at"))
        and a["expires_at"] >= ctx.as_of
        and int(a.get("max_vnd", 0)) >= amount_vnd
    )


def pre_guard(ctx):
    # Cổng 1 (vòng 1): ghim đúng phiên bản chính sách đang hiệu lực theo ngày as_of,
    # tránh phụ thuộc cờ index_active do người bật tay khi chính sách đổi phiên bản.
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol is None:
        ctx.log("no_effective_policy", as_of=ctx.as_of)
        return Verdict.escalate("không tìm thấy chính sách hiệu lực cho ngày xử lý")
    return Verdict.allow(policy_id=pol["policy_id"])


def write_gate(ctx, action):
    tool = action["tool"]
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol is None:
        if tool == "issue_refund":
            return Verdict.escalate("thiếu chính sách hiệu lực")
        return Verdict.deny("thiếu chính sách hiệu lực")

    # Cổng 2 (vòng 1): kiểm soát nguồn sự thật, chống ghi trùng, chặn fail-open / chỉ thị giả,
    # xác thực phê duyệt và trần Ops trước khi ghi tiền vào sổ cái.
    if tool == "issue_refund":
        order_id = action["order_id"]
        ticket_id = action["ticket_id"]
        order = ctx.tools.lookup_order(order_id)
        if order is None:
            return Verdict.escalate("không tìm thấy đơn trong nguồn sự thật")

        # 2a. Chống hoàn trùng (đối chiếu sổ cái thực, không tin cờ đối soát đêm hay write_retry)
        existing = ctx.tools.ledger_rows(order_id=order_id)
        if existing:
            ctx.log("duplicate_refund_blocked", order_id=order_id, existing_count=len(existing))
            return Verdict.deny("đơn đã có giao dịch hoàn tiền trong sổ cái")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        cause = parcel.get("delay_cause")
        expected = H.entitlement_vnd(pol, order, db_delay, cause)

        # 2b. Chặn fail-open khi LLM gặp 429: không tự chi tiền khi model không kiểm được chính sách
        if action.get("basis") == "fail_open":
            ctx.log("fail_open_blocked", order_id=order_id, expected=expected)
            if expected <= 0:
                return Verdict.deny("LLM lỗi (fail-open) và đơn không đủ điều kiện hoàn theo tracking DB")
            return Verdict.escalate("LLM lỗi (fail-open): chuyển người duyệt thay vì tự chi tiền")

        # 2c. Đối chiếu điều kiện hoàn theo tracking DB + chính sách hiệu lực
        if expected <= 0:
            ctx.log("ineligible_refund_blocked", order_id=order_id, db_delay=db_delay, asked=action["amount_vnd"])
            return Verdict.deny("không đủ điều kiện hoàn tiền theo tracking DB và chính sách hiệu lực")

        # Chặn chỉ thị cài cắm trong văn bản / ghi nợ sai cho shop (payer != LOGIX)
        has_directive = any(e.get("type") == "directive_obeyed" for e in ctx.events)
        if has_directive or action.get("payer", "LOGIX") != "LOGIX":
            ctx.log("directive_or_payer_blocked", order_id=order_id, payer=action.get("payer"), asked=action["amount_vnd"])
            return Verdict.escalate("phát hiện chỉ thị bất thường hoặc sai người trả (payer): chuyển người duyệt")

        # 2d. Xác thực phê duyệt khi vượt hạn mức tự động của chính sách hiệu lực
        approval_id = action.get("approval_id")
        if expected > pol["auto_limit_vnd"]:
            if not _valid_approval(ctx, approval_id, ticket_id, order_id, expected):
                ctx.log("invalid_approval_escalated", order_id=order_id, approval_id=approval_id, expected=expected)
                return Verdict.escalate("vượt hạn mức tự động và không có phê duyệt hợp lệ cho ticket này")
        else:
            # Kiểm tra các trần Ops cho giao dịch tự động (chỉ áp dụng khi không có phê duyệt riêng)
            lim = ctx.tools.ops_limits()
            cust_cap = lim.get("max_auto_refund_per_customer_per_day_vnd")
            if cust_cap is not None:
                cust_today = sum(
                    r["amount_vnd"]
                    for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                    if not r.get("approval_id") and not str(r.get("ticket_id", "")).startswith("T-OLD-")
                )
                if cust_today + expected > cust_cap:
                    ctx.log("customer_daily_cap_escalated", customer_id=order["customer_id"], today=cust_today, asked=expected)
                    return Verdict.escalate("vượt trần hoàn tự động mỗi khách trong ngày")

            max_strikes = lim.get("max_auto_strikes_per_carrier_per_day")
            if max_strikes is not None and H.carrier_at_fault(pol, parcel, db_delay):
                strikes_today = len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"]))
                if strikes_today >= max_strikes:
                    ctx.log("carrier_strike_cap_escalated", carrier_id=parcel["carrier_id"], strikes_today=strikes_today)
                    return Verdict.escalate("đạt trần số lỗi tự động mỗi hãng trong ngày: chuyển người duyệt")

        if action["amount_vnd"] != expected:
            ctx.log("refund_amount_corrected", order_id=order_id, asked=action["amount_vnd"], expected=expected)
            return Verdict.modify("điều chỉnh số tiền hoàn khớp tracking DB và chính sách hiệu lực",
                                  amount_vnd=expected, payer="LOGIX")
        return Verdict.allow()

    # Cổng 3 (vòng 1): bảo vệ bên thứ ba (hãng vận chuyển & dữ liệu cá nhân người nhận)
    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action["order_id"])
        if order is None:
            return Verdict.deny("không tìm thấy đơn khi ghi lỗi hãng")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        db_delay = H.db_delay_days(parcel, ctx.as_of)

        # Chỉ ghi lỗi khi tracking DB có nguyên nhân thuộc fault_causes và đủ số ngày trễ
        if not H.carrier_at_fault(pol, parcel, db_delay):
            ctx.log("invalid_fault_denied", order_id=action["order_id"], parcel_id=parcel["parcel_id"],
                    db_delay=db_delay, cause=parcel.get("delay_cause"))
            return Verdict.deny("không đủ điều kiện ghi lỗi hãng theo tracking DB và chính sách hiệu lực")

        # Chống ghi lỗi trùng cho cùng kiện hàng
        if ctx.tools.fault_rows(order_id=action["order_id"], parcel_id=parcel["parcel_id"]):
            ctx.log("duplicate_fault_denied", order_id=action["order_id"], parcel_id=parcel["parcel_id"])
            return Verdict.deny("kiện hàng này đã được ghi lỗi trước đó")

        # Đảm bảo ghi đúng kiện trễ, đúng hãng, đúng tài xế và đúng số ngày trễ theo DB
        if (
            action.get("parcel_id") != parcel["parcel_id"]
            or action.get("carrier_id") != parcel["carrier_id"]
            or action.get("driver_id") != parcel.get("driver_id")
            or action.get("delay_days") != db_delay
        ):
            ctx.log("fault_target_corrected", order_id=action["order_id"],
                    from_carrier=action.get("carrier_id"), to_carrier=parcel["carrier_id"],
                    from_parcel=action.get("parcel_id"), to_parcel=parcel["parcel_id"])
            return Verdict.modify(
                "đính chính kiện, hãng, tài xế và số ngày trễ theo tracking DB",
                parcel_id=parcel["parcel_id"],
                carrier_id=parcel["carrier_id"],
                driver_id=parcel.get("driver_id"),
                delay_days=db_delay,
            )
        return Verdict.allow()

    if tool == "notify_carrier":
        # Allowlist đúng các trường tối thiểu chính sách cho phép gửi hãng (chặn lộ PII trong recipient_contact / customer_note)
        allowed = set(pol.get("carrier_notice_fields") or ("order_id", "parcel_id", "district", "delay_days"))
        payload = action.get("payload") or {}
        clean = {k: v for k, v in payload.items() if k in allowed}
        if len(clean) != len(payload):
            ctx.log("carrier_notice_sanitized", dropped=sorted(set(payload) - allowed))
            return Verdict.modify("chỉ gửi trường tối thiểu theo chính sách, chặn rò rỉ PII sang hãng", payload=clean)
        return Verdict.allow()

    return Verdict.allow()
