# Phân tích Lab 10 và phân chia công việc cho 3 người

## 1. Mục tiêu bài lab

Nhóm xây dựng hồ sơ quyết định **Gate 1** cho trợ lý hoàn tiền của LogiX-VN: xác định tiêu chí chấp nhận trước khi xem kết quả, đo chất lượng và rủi ro, thiết kế các cổng kiểm soát, xử lý một thẻ sự cố, rồi đưa ra quyết định **v1** và **v2** về việc có chạy pilot hay không.

Lab kéo dài 240 phút. Sản phẩm cuối gồm ba phiếu A/B/C, code và cấu hình cổng, bằng chứng chạy đánh giá, `TEAM.md`, `submission/submission.json` và thư mục bài nộp được lệnh kiểm tra gom lại.

## 2. Phân công ba thành viên

| Thành viên | Vai trò | Việc chính | File/phần phụ trách |
|---|---|---|---|
| **Người 1** | Kỹ sư cổng | Chạy eval/trace/grade; ghi mã lần chạy và kết quả; viết 2–3 cổng phòng ngừa vòng 1; sửa cổng vòng 2 theo sự cố; thêm chỉ số theo dõi; phối hợp cả nhóm đọc trace. | `lab10/guards.py`, `lab10/monitors.py`, Phiếu B (B0–B2, phần kỹ thuật), Phiếu C (bằng chứng chạy, phần sửa và monitor) |
| **Người 2** | Sản phẩm và kinh doanh | Xác định mục tiêu và tiêu chí; thống nhất ngưỡng cùng nhóm; ký tiêu chí trước lần eval đầu tiên; phân tích bản đồ dữ liệu và drift; đặt giới hạn kinh doanh; tham gia quyết định Gate v1/v2. | `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`, Phiếu A, Phiếu B (B3 và phần kinh doanh của B8), Phiếu C (phân tích chi phí/phạm vi, quyết định C12) |
| **Người 3** | Vận hành và pháp lý | Điền thông tin thành viên; phân tích HAZOP; làm checklist go-live có PIC; đặt cổng vận hành/pháp lý; viết runbook; hoàn thiện dữ liệu nộp và kiểm tra checklist cuối. | `TEAM.md`, `config/operating_gates.json` mục `operations` và `legal`, Phiếu B (B4–B5, B7.5–B7.6), Phiếu C (runbook/C11), `submission/submission.json` |

**Cả nhóm cùng chịu trách nhiệm:** thống nhất tiêu chí và ngưỡng; pre-mortem; quyết định v1/v2; rà soát bằng chứng; điền các phiếu; chuẩn bị demo. Phân công là người cầm bút chính, không phải người duy nhất tham gia nội dung.

## 3. Tiến độ theo thời gian lab

| Thời gian | Công việc | Phân công và đầu ra |
|---|---|---|
| **0–15 phút** | Chuẩn bị và chia vai | Người 3 điền bảng thành viên/vai trong `TEAM.md`; cả nhóm kiểm tra repo, môi trường và thống nhất cách phối hợp. |
| **15–60 phút** | Khối 1: mục tiêu, thước đo, tiêu chí | Cả nhóm hoàn thành Phiếu A. Người 2 cầm bút chính và nhập ngưỡng vào `config/acceptance_criteria.json`; Người 1 góp ý metric kỹ thuật; Người 3 góp ý mục tiêu vận hành và pháp lý. |
| **60–65 phút** | Ký tiêu chí | Người 2 chạy lệnh ký; nhóm commit/push tiêu chí. **Không chạy eval trước khi ký. Sau khi ký không sửa tiêu chí.** |
| **65–85 phút** | Khối 2A: đo và phân tích rủi ro | Người 1 chạy baseline/gate/trace và ghi Phiếu B; Người 2 làm bản đồ dữ liệu, drift; Người 3 làm HAZOP và checklist. Cả nhóm hoàn thành pre-mortem. |
| **85–105 phút** | Khối 2B: dựng cổng vòng 1 | Người 1 sửa `lab10/guards.py`; Người 2 điền phần `business`; Người 3 điền `operations`/`legal` và runbook phần đầu. Sau đó chạy các kiểm tra được README yêu cầu. |
| **105–115 phút** | Chốt vòng 1 và quyết định v1 | Cả nhóm đối chiếu số liệu và quyết định; Người 1 chạy checkpoint/eval theo hướng dẫn; Người 2/3 hoàn thiện B8. Commit/push bản đã chốt. |
| **115–125 phút** | Nghỉ | Giữ nguyên các bản đã chốt. |
| **125–185 phút** | Khối 3: thẻ sự cố, phân tích và sửa | Cả nhóm nhận đúng thẻ và ghi số thẻ. Chạy mốc `prepared` trước khi sửa. Người 1 xử lý code, trace và monitor; Người 2 phân tích tác động kinh doanh; Người 3 phân tích vận hành/pháp lý và cập nhật runbook. Cả nhóm điền Phiếu C. |
| **185–200 phút** | Quyết định v2 và gom bài | Cả nhóm chốt quyết định v2 và ba dòng bắt buộc. Người 3 hoàn thiện `submission/submission.json`; nhóm chạy lệnh gom/kiểm tra và sửa mục thiếu. |
| **200–230 phút** | Demo | Trình bày ba mốc `base · prepared · after`, giải thích quyết định bằng số liệu và tiêu chí đã ký. |
| **230–240 phút** | Đẩy bài cuối | Commit/push repo và kiểm tra thư mục nộp. Mỗi thành viên tự gửi link repo trên LMS trước hạn. |

## 4. Các phụ thuộc quan trọng

1. **Ký tiêu chí trước lần eval đầu tiên.** Đây là yêu cầu bắt buộc; lịch sử Git và nhật ký chạy được dùng để đối chiếu.
2. **Chốt cổng vòng 1 trước khi xử lý sự cố.** Lệnh checkpoint tạo bản lưu cổng vòng 1; giữ bản đó nguyên vẹn.
3. **Chạy `prepared` trước khi sửa theo thẻ.** Mốc này cho biết cổng vòng 1 đã giúp được gì; sau đó mới chạy `after` để đo tác động sửa đổi.
4. **Mọi kết luận phải gắn bằng chứng.** Ghi mã lần chạy, ticket/seed, metric và dòng trace liên quan vào phiếu.
5. **Thông tin nhóm phải nhất quán.** Tên repo, trường `team` trong tiêu chí và trong `submission/submission.json` phải giống nhau; `members` phải khớp `TEAM.md` và có MSSV.
6. **Hoàn thiện đủ hồ sơ.** Điền Phiếu A/B/C theo các mục áp dụng, cập nhật `TEAM.md`, rồi chạy công cụ gom/kiểm tra tới khi báo `ĐỦ THÀNH PHẦN`.

## 5. Checklist bàn giao cuối

- [ ] `TEAM.md` có tên đầy đủ, MSSV, vai và mục đóng góp của từng thành viên.
- [ ] Tiêu chí đã ký, commit và push trước lần chạy eval đầu tiên.
- [ ] Cổng vòng 1 đã checkpoint trước mốc phút 115.
- [ ] Đã chạy và lưu bằng chứng cho các mốc cần thiết: `base`, `prepared`, `after`.
- [ ] Ba phiếu A/B/C đã điền đủ các mục áp dụng; ghi đúng số thẻ sự cố.
- [ ] `submission/submission.json` có đủ trường và khớp thông tin thành viên.
- [ ] Lệnh kiểm tra bài báo `ĐỦ THÀNH PHẦN`; các report và nhật ký chạy nằm trong `submission/runs/`.
- [ ] Repo đã push; **từng thành viên** đã nộp link repo trên LMS.

## 6. Lưu ý theo quy định lab

AI được phép hỗ trợ đọc code, gợi ý cách viết cổng và rà soát câu chữ, nhưng không được dùng để viết xử lý riêng theo ticket hoặc câu chữ cụ thể. Các ngưỡng, cấu hình và quyết định phải do nhóm lựa chọn và giải thích được. Mỗi thành viên ghi rõ đóng góp và việc sử dụng AI (nếu có) trong mục cá nhân ở `TEAM.md`.
