# T25 — Chạy ma trận sensitivity và benchmark

P5 · Luồng A+B · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Chạy nhiều size/support/partitions trên môi trường đã mô tả, lưu dữ liệu thô ngoài Git. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/experiment_protocol.md`
- `src/ie212_instacart/benchmark/runner.py`

Trước bắt đầu cần T24. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `experiments/configs/sensitivity.toml`
- `reports/benchmark_runs.md`

Mỗi cấu hình khả thi có ít nhất ba lần đo; ghi biến thiên, thất bại và workload.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T25`
- Output `python scripts/tasks/check_output.py T25`
- Merge `bash scripts/ci/validate_merge.sh main T25`

Test nghiệm thu `tests.test_t25`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Cần dữ liệu, thời gian máy, cấu hình HDFS và xác nhận chạy thực nghiệm.
