# T12 — Chuẩn hóa từng order thành basket Spark

P2 · Luồng A · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Dùng Spark SQL/DataFrame join khóa, loại trùng và sắp xếp item theo order_id. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/data_contract.md`
- `src/ie212_instacart/ingestion/profile.py`

Trước bắt đầu cần T11. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/preprocessing/baskets.py`
- `tests/test_t12.py`

Kiểm không gộp order cùng user, không cắt basket, không join nhầm split.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T12`
- Output `python scripts/tasks/check_output.py T12`
- Merge `bash scripts/ci/validate_merge.sh main T12`

Test nghiệm thu `tests.test_t12`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ audit dữ liệu và contract.
