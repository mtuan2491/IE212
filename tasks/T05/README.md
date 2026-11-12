# T05 — Xây registry và kiểm chứng task gates

P0 · Luồng B · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Chạy gate trên fixture và test mã thoát cho dependency, schema, output và merge. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/ie307_workflow_review.md`
- `pyproject.toml`

Trước bắt đầu cần T02, T04. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `tasks/registry.toml`
- `scripts/tasks/check_input.py`
- `scripts/tasks/check_output.py`
- `scripts/tasks/validate_contracts.py`
- `scripts/ci/validate_merge.sh`
- `scripts/ci/run_tests.sh`
- `tests/test_bootstrap.py`

Phát hiện cycle, path sai và xung đột. Kiểm tra không đổi working tree/main.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T05`
- Output `python scripts/tasks/check_output.py T05`
- Merge `bash scripts/ci/validate_merge.sh main T05`

Test nghiệm thu `tests.test_bootstrap`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ repository sạch và review.
