# T19 — Đối chiếu DApriori và FP-Growth theo k≤2

P4 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Dùng cùng basket, ngưỡng và itemset chuẩn hóa để so tần suất/support từng khóa. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `src/ie212_instacart/mining/fpgrowth.py`
- `src/ie212_instacart/mining/dapriori.py`

Trước bắt đầu cần T15, T18. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/validation/itemset_parity.py`
- `tests/test_t19.py`

Kiểm đủ tập khóa và giá trị. Ghi FP-Growth có khai phá độ dài lớn hơn trước lọc hay không.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T19`
- Output `python scripts/tasks/check_output.py T19`
- Merge `bash scripts/ci/validate_merge.sh main T19`

Test nghiệm thu `tests.test_t19`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ hai implementation đã review.
