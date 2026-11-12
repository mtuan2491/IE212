# Registry IE212

ID task gồm chữ T và đúng hai chữ số, ví dụ `T01`. Mỗi T01–T29 có `task.toml`, tài liệu và issue draft. `DEMO` dùng riêng cho bootstrap. Trạng thái theo vòng đời planned, todo, ready, in_progress, blocked, in_review, done. `dependencies` là điều kiện bắt đầu. `merge_dependencies` phải được nghiệm thu và có trên base trước tích hợp, cùng các dependency bắt đầu.

Chạy `python scripts/tasks/check_input.py Txx`, `python scripts/tasks/check_output.py Txx` và `bash scripts/ci/validate_merge.sh main Txx`. Mã thoát 0 PASS, 1 FAIL, 2 BLOCKED. Gate chỉ chạy argv unittest từ contract đã review và xác minh tệp trước khi gọi test. Txx có test đang planned sẽ BLOCKED cho đến khi module kiểm chứng tồn tại.

Sau review thật, dependency done cần `tasks/Txx/review.toml` có `reviewed_by`, `commit` và `evidence` trỏ đến file trong repo, đồng thời đủ output đã bàn giao. Đừng commit raw data hay output lớn. Evidence có thể ghi hash và URI của artifact trong run đã kiểm.
