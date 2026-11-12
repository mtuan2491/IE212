# T16 — Sinh và kiểm tra luật kết hợp

P3 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Ánh xạ tên sản phẩm và kiểm Support, Confidence, Lift từ các tần suất gốc. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `src/ie212_instacart/mining/fpgrowth.py`
- `docs/data_contract.md`

Trước bắt đầu cần T15. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/mining/rules.py`
- `tests/test_t16.py`

Có test luật cụ thể, ngưỡng bằng nhau và tên sản phẩm thiếu.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T16`
- Output `python scripts/tasks/check_output.py T16`
- Merge `bash scripts/ci/validate_merge.sh main T16`

Test nghiệm thu `tests.test_t16`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ baseline itemsets.
