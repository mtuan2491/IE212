# T17 — Xác minh parity của FP-Growth và luật

P3 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Đối chiếu từng khóa itemset/luật và chỉ số với oracle trong lần chạy tái lập. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `src/ie212_instacart/validation/oracle.py`
- `src/ie212_instacart/mining/rules.py`

Trước bắt đầu cần T14, T15, T16. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `tests/test_t17.py`
- `docs/validation/fpgrowth.md`

Sai một hàng làm kiểm thử fail, ghi seed và phạm vi fixture.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T17`
- Output `python scripts/tasks/check_output.py T17`
- Merge `bash scripts/ci/validate_merge.sh main T17`

Test nghiệm thu `tests.test_t17`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ oracle, FP-Growth và luật.
