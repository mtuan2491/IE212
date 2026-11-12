# T22 — So toàn bộ output Spark và Hadoop MapReduce

P4 · Luồng A+B · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Chuẩn hóa khóa và so từng số đếm của hai output trên cùng tập basket. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `mapreduce/src/main/java/ie212/PairCount.java`
- `src/ie212_instacart/mining/pair_count.py`

Trước bắt đầu cần T20, T21. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/validation/pair_parity.py`
- `tests/test_t22.py`

Báo thiếu, thừa, sai giá trị. Kiểm boundary và lưu nguồn input/config.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T22`
- Output `python scripts/tasks/check_output.py T22`
- Merge `bash scripts/ci/validate_merge.sh main T22`

Test nghiệm thu `tests.test_t22`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ hai job và môi trường test tương ứng.
