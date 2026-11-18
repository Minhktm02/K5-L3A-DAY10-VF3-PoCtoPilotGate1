"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def policy_drift_override_rate(trials):
    """Tỉ lệ lần chạy mà pre_guard phát hiện chính sách hiệu lực theo ngày lệch cờ index_active."""
    hits = sum(
        any(e.get("type") == "guard" and e.get("kind") == "stale_policy_overridden" for e in t["events"])
        for t in trials
    )
    return hits / max(1, len(trials))


def unrecorded_cause_rate(trials):
    """Tỉ lệ lần chạy có sự kiện tracking nhưng trường delay_cause trong DB bị trống (cause_recorded=False)."""
    tracked = [t for t in trials if any(e.get("type") == "tracking" for e in t["events"])]
    if not tracked:
        return 0.0
    missing = sum(
        any(e.get("type") == "tracking" and e.get("cause_recorded") is False for e in t["events"])
        for t in tracked
    )
    return missing / len(tracked)


def max_carrier_strikes_per_day(trials):
    """Số lỗi tự động tối đa ghi cho cùng một hãng vận chuyển trong một ngày giả lập (seed, day, carrier_id)."""
    counts = {}
    for t in trials:
        for f in t["faults"]:
            key = (t["seed"], t["day"], f["carrier_id"])
            counts[key] = counts.get(key, 0) + 1
    return float(max(counts.values(), default=0))


def carrier_strike_cap_hit_rate(trials):
    """Tỉ lệ lần chạy bị cổng chặn/chuyển do chạm trần lỗi tự động/hãng/ngày."""
    hits = sum(
        any(
            e.get("type") == "guard"
            and e.get("kind") in ("carrier_strike_cap_denied", "carrier_strike_cap_escalated")
            for e in t["events"]
        )
        for t in trials
    )
    return hits / max(1, len(trials))


def model_override_rate(trials):
    """Tỉ lệ lần chạy mà model lấy số ngày trễ khách tự khai đè lên tracking DB (bắt lỗi chìm ngoài thẻ)."""
    hits = sum(any(e.get("type") == "model_override" for e in t["events"]) for t in trials)
    return hits / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,                 # có sẵn; KHÔNG tính là metric mới của đội
    "policy_drift_override_rate": policy_drift_override_rate,
    "unrecorded_cause_rate": unrecorded_cause_rate,
    "max_carrier_strikes_per_day": max_carrier_strikes_per_day,
    "carrier_strike_cap_hit_rate": carrier_strike_cap_hit_rate,
    "model_override_rate": model_override_rate,
}
STARTER_MONITORS = ("escalation_rate",)
