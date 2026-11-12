# T03 — Chốt phạm vi và truy vết yêu cầu

P0 · Luồng Chung · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Ánh xạ từng yêu cầu mục 1 sang task hoặc bằng chứng dự kiến. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/requirements.md`
- `docs/reset_verification.md`

Trước bắt đầu cần T01. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/requirements.md`
- `docs/open_questions.md`

Giữ DOI, prior/full, HDFS và hai trục so sánh. Ghi riêng câu hỏi về góp ý giảng viên.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T03`
- Output `python scripts/tasks/check_output.py T03`
- Merge `bash scripts/ci/validate_merge.sh main T03`

Test nghiệm thu `tests.test_t03`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ xác minh reset và review yêu cầu.
