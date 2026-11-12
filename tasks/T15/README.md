# T15 — Chạy Parallel FP-Growth bằng Spark MLlib

P3 · Luồng A · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Fit FP-Growth và xuất items/freq/support cùng provenance. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `src/ie212_instacart/preprocessing/baskets.py`
- `src/ie212_instacart/validation/oracle.py`

Trước bắt đầu cần T12, T14. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/mining/fpgrowth.py`
- `tests/test_t15.py`

Khớp oracle theo scope fixture. Ghi phiên bản Spark và phạm vi itemset API xử lý.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T15`
- Output `python scripts/tasks/check_output.py T15`
- Merge `bash scripts/ci/validate_merge.sh main T15`

Test nghiệm thu `tests.test_t15`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ basket và oracle.
