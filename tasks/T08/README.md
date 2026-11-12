# T08 — Thiết lập và kiểm tra HDFS pseudo-distributed

P1 · Luồng B · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Ghi setup và chạy put/get checksum trong namespace thử nghiệm được cấp. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/runbooks/runtime.md`

Trước bắt đầu cần T07. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/runbooks/hdfs.md`
- `scripts/bootstrap/check_hdfs.py`

Phân biệt URI HDFS và file; kiểm round trip và báo BLOCKED khi thiếu daemon.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T08`
- Output `python scripts/tasks/check_output.py T08`
- Merge `bash scripts/ci/validate_merge.sh main T08`

Test nghiệm thu `tests.test_t08`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Cần phê duyệt cài đặt nếu chưa có Hadoop và xác định namespace.
