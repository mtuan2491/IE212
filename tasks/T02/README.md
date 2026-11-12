# T02 — Khảo sát quy trình IE307

P0 · Luồng B · Phạm vi XS · Owner unassigned

## Mục tiêu và phạm vi

Ghi bằng chứng quy trình task, CI, preflight và merge theo tệp nguồn đã đọc. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/requirements.md`

Trước bắt đầu cần xác nhận đầu vào tại chỗ. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/ie307_workflow_review.md`

Mỗi quy ước áp dụng có file đối chiếu, điều chỉnh cho hai người và giới hạn khảo sát.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T02`
- Output `python scripts/tasks/check_output.py T02`
- Merge `bash scripts/ci/validate_merge.sh main T02`

Test nghiệm thu `tests.test_t02`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ review tài liệu khảo sát.
