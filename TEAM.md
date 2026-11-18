# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `VF3`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-VF3-PoCtoPilotGate1` (https://github.com/Minhktm02/K5-L3A-DAY10-VF3-PoCtoPilotGate1)
- Thẻ sự cố đã bốc (S1–S8): `S3`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Trương Việt Công | 2A202603585 | Vận hành và pháp lý | X |
|   2 | Khuất Tiến Minh | 2A202603616 | Kỹ sư cổng | |
|   3 | Đào Quang Huy | 2A202603642 | Sản phẩm và kinh doanh | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## TruongVietCong-2A202603585

### Phần việc phụ trách

Vai **Vận hành và pháp lý** (Trưởng nhóm): câu 1.2, 1.4 trong Phiếu A (`templates/form-a-criteria.md`); câu 2.4 (HAZOP vòng 1 mục B4, checklist 9 nhóm việc mục B5), lăng kính con người/vận hành & pháp lý của pre-mortem (B6), câu 2.10 (cổng `operations` & `legal` trong `config/operating_gates.json`, Runbook 1–3 mục B7.5 và Giờ cao điểm mục B7.6); Vòng 2 thẻ S3: mục C3.5 (mở lại bản đồ dữ liệu), C4 (HAZOP của thẻ), C5 câu 3.3 (giả định môi trường), C10 (Risk register), C11 (cập nhật checklist 9 nhóm việc & Runbook 4–5), hoàn thiện `submission/submission.json` và gom bài nộp `submission/`.

### Đóng góp cụ thể

- Thiết lập đầy đủ cổng vận hành & pháp lý trong `config/operating_gates.json` (`pic: NV-TUNG`, `approver_id: NV-HANH`, `reviewers_on_shift: 1`, `review_capacity_per_hour: 6`, `max_queue_wait_minutes: 60`, `decision_note: true`, `review_sampling_pct: 10`, `pii_fields_blocked_to_third_party: ["recipient_contact", "customer_note"]`, `carrier_fault_requires_recorded_cause: true`).
- Xây dựng HAZOP mở rộng (vòng 1 cho `notify_carrier` và vòng 2 cho `file_carrier_fault` trên S3), checklist 9 nhóm việc có PIC cụ thể cho từng dòng, Risk register 2 dòng đổi được quyết định Gate, và Runbook đầy đủ phần 1–5 + kịch bản giờ cao điểm.
- Phối hợp gom và kiểm chứng bài nộp với `python -m lab10.check_submission --collect` đạt `ĐỦ THÀNH PHẦN`.
- **Sử dụng AI (theo `RULES.md`):** Dùng trợ lý AI để rà soát cấu trúc HAZOP, đối chiếu các khoá trong `config/operating_gates.json` với `data/world.json`, và soát nhất quán câu chữ giữa Runbook 1–5 với report; toàn bộ con số ngưỡng vận hành/pháp lý do nhóm tự chốt và kiểm chứng.

### Bằng chứng

- Commit: `4e692de` (`add team.md`), `44d8b2e` (`van hanh va phap ly vong 1`, PR #3 `11ffd2f`), `a43ec35` (chốt vòng 1 `1bde102a`), và commit nộp bài vòng 2 S3.
- File & mục phiếu: `config/operating_gates.json`, `templates/form-a-criteria.md` (A1.2, A2 Telemetry), `templates/form-b-evaluation-gates.md` (B4, B5, B6, B7.5, B7.6), `templates/form-c-incident.md` (C3.5, C4, C5.3.3, C10, C11), `submission/submission.json`.

### Exit ticket

- **Một điều học được:** Đặt đúng cổng pháp lý (`carrier_fault_requires_recorded_cause = true`, chặn PII) và điều kiện lòng tin vận hành (`decision_note = true`, kiểm mẫu 10%, đúng `approver_id`) ngay ở vòng 1 giúp ngăn thiệt hại cho bên thứ ba mà không làm vỡ SLA hàng chờ.
- **Một điều còn chưa chắc:** Cách đo thực tế tỉ lệ sai lệch nhập tay `delay_cause` tại điểm phát vùng bão khi pilot thật và ngưỡng cảnh báo tối ưu cho bộ đếm lỗi hãng cửa sổ 7 ngày lăn.

## KhuatTienMinh-2A202603616

### Phần việc phụ trách

Vai **Kỹ sư cổng**: câu 1.3 (offline metric bước ghi lỗi hãng) và góp ý ranh giới đầu ra (A4) trong Phiếu A; Khối 2A–2B: chạy baseline `eval`/`gate`/`trace T-002@55` (B0, B1, B2), pre-mortem kỹ thuật (B6), code 3 cổng phòng ngừa vòng 1 trong `lab10/guards.py` (B7.1), câu 2.7 chống rò rỉ dữ liệu (B7.2), câu 2.8 behavioral test với 2 ticket `--adhoc` (B7.3), chốt `lab10.checkpoint` (`prepared`); Khối 3 thẻ S3: trace 8 ticket hỏng mốc `base` (`S3-01, S3-02, S3-04, S3-20, S3-40..S3-43`), tối ưu `lab10/guards.py` vòng 2, bổ sung 5 chỉ số theo dõi mới vào `lab10/monitors.py`, điền Phiếu C (C0, C1, C2, C6, C7, C8, C9) và kiểm thử toàn bộ.

### Đóng góp cụ thể

- Viết 3 cổng phòng ngừa ngoài model trong `lab10/guards.py` hoàn toàn không hardcode: (1) `pre_guard` ghim chính sách hiệu lực theo `H.effective_policy` (đỡ sạch concept drift `REFUND-v3 → v4` của S3 ngay từ mốc `prepared`); (2) `write_gate(issue_refund)` chống trùng sổ cái, chặn `fail_open` & chỉ thị trừ shop, đối chiếu `entitlement_vnd` và xác thực `approval_id`; (3) `write_gate(file_carrier_fault, notify_carrier)` bắt buộc `H.carrier_at_fault`, đính chính đúng kiện/hãng/số ngày trễ và lọc allowlist PII.
- Vòng 2 (S3): tách kiểm soát trần `max_auto_strikes_per_carrier_per_day` từ `issue_refund` sang `file_carrier_fault` (`deny` từ lỗi thứ 3+, giữ nguyên hoàn phí cho khách), giúp `escalation_rate` trên S3 giảm từ `0,25 → 0,0833`, chi phí giảm `6.038đ → 4.405đ/ticket`, ROI tăng `0,66 → 1,27` mà vẫn giữ `pass_rate = 1,0` và 0 regression trên bộ nền (`13/13` unit tests OK).
- Bổ sung 5 chỉ số theo dõi không nhãn mới vào `lab10/monitors.py` (tổng 6 chỉ số trong `MONITORS`: thêm `policy_drift_override_rate`, `unrecorded_cause_rate`, `max_carrier_strikes_per_day`, `carrier_strike_cap_hit_rate`, `model_override_rate`), tất cả đều sáng đèn (`6 monitor ✅`).
- **Sử dụng AI (theo `RULES.md`):** Dùng trợ lý AI để đọc mã nguồn `lab10/agent.py`/`tools.py`/`helpers.py`, gợi ý cấu trúc cổng phòng ngừa tổng quát không hardcode trong `guards.py`/`monitors.py` và hỗ trợ tổng hợp kết quả trace; mọi lệnh đo, kiểm thử và xác minh đều chạy thực tế trên máy.

### Bằng chứng

- Commit: `2c3babc` & `b1db968` (PR #2 `aa59ba1`), `a43ec35` (chốt vòng 1 `1bde102a`), `ba07346` (`Nhận thẻ S3`), và commit hoàn tất vòng 2 S3.
- Mã lần chạy: `R-base-before-20261118-155816-bd5d41`, `R-base-after-20261118-161207-949478`, `R-base-prepared-20261118-164500-d123e9`, `R-S3-grade-20261118-170611-d123e9`, `R-S3-after-20261118-171954-ce7daa`, `R-base-after-20261118-171954-ce7daa`, và lần grade cuối S3.

### Exit ticket

- **Một điều học được:** Đặt gate đúng tầng và đúng thao tác ghi quyết định cả an toàn lẫn hiệu quả kinh doanh — cùng một trần 2 lỗi/hãng/ngày, đặt ở `issue_refund` gây escalate thừa làm đội chi phí, còn đặt ở `file_carrier_fault` vừa bảo vệ hãng vừa trả đủ tiền hoàn cho khách và nâng ROI gần gấp đôi.
- **Một điều còn chưa chắc:** Cách mở rộng kiến trúc `write_gate` trong hệ thống phân tán thực tế (nhiều worker chạy song song) để đếm chính xác trần lỗi/hãng/ngày và chống ghi trùng sổ cái không bị race condition.

## DaoQuangHuy-2A202603642

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh**: soạn thảo và ký Bản tiêu chí chấp nhận (`config/acceptance_criteria.json`, Phiếu A mục A1.1, A3, A4, A5 — commit `6027ce7`); Khối 2A–2B: lập bản đồ dữ liệu và dự báo concept drift `REFUND-v3 → v4` (B3), pre-mortem lăng kính kinh doanh (B6), thiết lập cổng `business` trong `config/operating_gates.json` (B7.4), chốt Quyết định Gate 1 · v1 (B8); Khối 3 thẻ S3: viết Specification (C5 câu 3.2), đánh giá tác động chi phí/ROI/phân khúc kho–hãng, viết Quyết định Gate 1 · v2 và 3 dòng bắt buộc (C12).

### Đóng góp cụ thể

- Thiết lập và ký niêm phong Bản tiêu chí chấp nhận (`8d87f12a`) trước lần chạy đầu tiên với đầy đủ 5 ngưỡng `required`, `escalation_rate_max`, 3 ngưỡng `business_ops` (`cost_per_ticket_vnd_max = 7000`, `roi_min = 0.4`, `queue_stuck_max = 0`), `stop_condition` và `decision_rule` cho cả 4 quyết định.
- Dự báo chính xác kịch bản concept drift `REFUND-v3 → v4` ngày `01/12/2026` ngay từ vòng 1 (Phiếu B mục B3), làm cơ sở để Kỹ sư cổng dựng Cổng 1 ghim chính sách hiệu lực trước khi nhận thẻ S3.
- Thiết lập cổng `business` (`daily_refund_cap_vnd = 1500000`, `cost_budget_per_ticket_vnd = 1400`, `pilot_scope = all 100%`, `roi_min = 0.4`) và chốt Quyết định Gate 1 v1 (`Tiếp tục`) và v2 (`Tiếp tục`) khớp chặt chẽ với bằng chứng số liệu và tiêu chí đã ký.
- **Sử dụng AI (theo `RULES.md`):** Dùng trợ lý AI để soát cấu trúc câu tiêu chí, đối chiếu công thức chi phí/ROI từ `data/world.json` và biên tập nhất quán Phiếu A, B3, B7.4, C12; toàn bộ ngưỡng tiêu chí và quyết định Gate 1 v1/v2 do nhóm tự thống nhất và giải thích được.

### Bằng chứng

- Commit: `6027ce7` (`Sign acceptance criteria`), `cf7be79` (Phiếu A A1–A5), `76fc15d` (cổng `business` + B3, B7.4), `a8bda9a` (PR #1 `301b2f3`, B6 kinh doanh), `a43ec35` (quyết định v1), và commit hoàn tất vòng 2 S3 (C5.3.2, C12).
- File & mục phiếu: `config/acceptance_criteria.json`, `config/acceptance_criteria.lock`, `config/operating_gates.json` (`business`), `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md` (B3, B6, B7.4, B8), `templates/form-c-incident.md` (C5.3.2, C12).

### Exit ticket

- **Một điều học được:** Việc ký trước tiêu chí chấp nhận gồm cả nhóm `business_ops` (chi phí, ROI, ca ùn) giúp quyết định Gate 1 khách quan, không bị cảm tính kéo sang "Tiếp tục" khi còn lỗi an toàn hay lỗ vận hành.
- **Một điều còn chưa chắc:** Mức tăng thực tế của tỉ lệ chuyển người duyệt khi áp `auto_limit_vnd = 100.000đ` (`REFUND-v4`) trên tập đơn thật có giá trị hàng hoá cao ở kho DN và kho sỉ HCM-B2B.
