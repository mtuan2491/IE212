# T09 — Chốt schema, provenance và fixture CSV

P1 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Xác nhận schema từ nguồn đăng ký và tạo fixture nhỏ cho ca tốt/lỗi. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/requirements.md`
- `tests/fixtures/baskets.csv`

Trước bắt đầu cần T03. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/data_contract.md`
- `tests/fixtures/instacart/orders.csv`
- `scripts/data/verify_input.py`

Có assertions cho header, missing file, schema sai và checksum nguồn nếu có.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T09`
- Output `python scripts/tasks/check_output.py T09`
- Merge `bash scripts/ci/validate_merge.sh main T09`

Test nghiệm thu `tests.test_t09`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Cần xác minh metadata nguồn dataset.
