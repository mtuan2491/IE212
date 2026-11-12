# Quy định làm việc IE212

Đọc docs/requirements.md, docs/architecture.md, tasks/registry.toml và contract của task trước khi sửa. Yêu cầu đăng ký và chỉ dẫn hiện hành của chủ dự án có ưu tiên cao nhất. Ghi ADR, cập nhật contract và issue khi đổi phạm vi.

- Mỗi lượt một task đã có owner và dependency được review. Chạy `python scripts/tasks/check_input.py Txx` trước khi sửa. Khi BLOCKED, ghi lý do và xử lý đầu vào. Dùng nhánh `feat/Txx-…` hoặc `fix/Txx-…`.
- Dùng fixture có assertion theo acceptance criteria. Chạy output gate rồi merge gate. Thành viên còn lại review trước merge. Sau merge chạy smoke phù hợp trên main, ghi SHA, review, evidence, PR và giới hạn.
- Báo cáo task gồm tóm tắt, tệp sửa, trạng thái của ba gate, lệnh tái lập, giới hạn và link issue/PR. Chỉ ghi done khi AC bắt buộc đã có bằng chứng và có review thật. Giữ riêng PASS, FAIL, BLOCKED và NOT RUN.
- Giữ raw ở vùng được phép, lưu hash và provenance. Không commit dữ liệu lớn, secret, venv, HDFS runtime hoặc artifacts. Thao tác phá hủy, cài đặt hệ thống và xuất bản GitHub cần được chủ dự án cho phép.
- Giữ `prompt.md` và `prompt.txt` ở máy cục bộ. Bật hook Git theo README để kiểm tra trước commit và push.
- Ghi dataset/split, seed, phiên bản, commit, cấu hình/tài nguyên và lệnh thực nghiệm. DApriori k≤2 là triển khai giới hạn, kèm mapping và khác biệt với bài báo. FP-Growth là API Spark MLlib. Chỉ kết luận về thời gian trong điều kiện khối lượng công việc đã ghi rõ.
- Đối chiếu riêng Java Hadoop MapReduce và Spark trên cùng input và quy ước đếm cặp. CI fixture/local và kiểm HDFS/full/benchmark có evidence riêng.
- Điều phối thay đổi config và contract với cả hai thành viên. Dùng issue draft local cho tới khi remote/quyền và xuất bản được chủ dự án duyệt.
