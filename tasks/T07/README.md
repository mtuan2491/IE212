# T07 — Thử tương thích và pin môi trường

P1 · Luồng B · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Thử phiên bản Python, JVM, Spark, Hadoop và Git trên môi trường dự kiến. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `pyproject.toml`
- `config/example.toml`

Trước bắt đầu cần T04. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/runbooks/runtime.md`
- `requirements-runtime.txt`

Ghi ma trận đã thử, pin phiên bản và lưu output doctor cùng smoke test.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T07`
- Output `python scripts/tasks/check_output.py T07`
- Merge `bash scripts/ci/validate_merge.sh main T07`

Test nghiệm thu `tests.test_t07`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Cần biết môi trường triển khai và quyền cài đặt.
