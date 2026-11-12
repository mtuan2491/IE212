# T26 — Tổng hợp kết quả và vẽ biểu đồ

P5 · Luồng B · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Sinh summary CSV và chart từ run IDs thật, ghi điều kiện và giới hạn. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `reports/benchmark_runs.md`
- `docs/experiment_protocol.md`

Trước bắt đầu cần T25. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `scripts/experiments/summarize.py`
- `reports/results.md`

Đối chiếu thống kê với raw results, phân biệt local/pseudo-distributed và cluster.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T26`
- Output `python scripts/tasks/check_output.py T26`
- Merge `bash scripts/ci/validate_merge.sh main T26`

Test nghiệm thu `tests.test_t26`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ log thực nghiệm đã xác minh.
