# T23 — Tạo tập benchmark theo số order

P5 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Chọn order_id theo seed, tạo manifest và giữ tất cả sản phẩm mỗi order được chọn. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/data/instacart_manifest.json`
- `src/ie212_instacart/preprocessing/baskets.py`

Trước bắt đầu cần T10, T12. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/benchmark/subsets.py`
- `tests/test_t23.py`

Kiểm kích thước, không cắt basket, tái lập cùng seed và scope dữ liệu.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T23`
- Output `python scripts/tasks/check_output.py T23`
- Merge `bash scripts/ci/validate_merge.sh main T23`

Test nghiệm thu `tests.test_t23`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ prior/full và basket.
