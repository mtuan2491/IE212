# T14 — Viết oracle itemsets và luật bằng Python

P3 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Đếm vét cạn fixture và kiểm một luật cụ thể bằng count(A), count(B), count(A∪B). Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/data_contract.md`
- `tests/fixtures/instacart/orders.csv`

Trước bắt đầu cần T09. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/validation/oracle.py`
- `tests/test_t14.py`

Kiểm đúng tại biên ceil(s*N), frequency nguyên, support/confidence/lift.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T14`
- Output `python scripts/tasks/check_output.py T14`
- Merge `bash scripts/ci/validate_merge.sh main T14`

Test nghiệm thu `tests.test_t14`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ data contract và fixture.
