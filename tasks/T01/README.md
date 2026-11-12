# T01 — Kiểm kê và bảo toàn repo cũ

P0 · Luồng Chung · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Ghi HEAD/refs, file chưa commit và hash CSV/prompt trước và sau khi lưu trữ. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/requirements.md`

Trước bắt đầu cần xác nhận đầu vào tại chỗ. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/reset_verification.md`

Xác nhận archive và repo sạch có lịch sử riêng, kèm đường rollback.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T01`
- Output `python scripts/tasks/check_output.py T01`
- Merge `bash scripts/ci/validate_merge.sh main T01`

Test nghiệm thu `tests.test_t01`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ xác minh thao tác lưu trữ đã được chủ dự án duyệt.
