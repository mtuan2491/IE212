# T04 — Khởi tạo repository sạch

P0 · Luồng Chung · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Đưa cấu trúc bootstrap vào Git mới và giữ bản đặc tả gốc ở máy cục bộ. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/reset_verification.md`
- `docs/requirements.md`

Trước bắt đầu cần T01, T03. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `AGENTS.md`
- `README.md`
- `pyproject.toml`
- `config/example.toml`

Repo sạch có ref riêng khi có commit được duyệt và hướng dẫn chạy từ clone sạch.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T04`
- Output `python scripts/tasks/check_output.py T04`
- Merge `bash scripts/ci/validate_merge.sh main T04`

Test nghiệm thu `tests.test_t04`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Đã lưu trữ repo cũ và khởi tạo Git tại đường dẫn mới. Còn chờ review T01, T03 và nghiệm thu từ bản clone sạch.
