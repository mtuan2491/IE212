# T06 — Đọc và đối chiếu Algorithm 1 của DApriori

P1 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Ánh xạ từng bước Algorithm 1 đến phép Spark dự kiến và chỉ ra khác biệt. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/requirements.md`

Trước bắt đầu cần T03. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/research.md`
- `docs/adr/0002-dapriori-scope.md`

Trích DOI/phiên bản, công bố rõ giới hạn k và các bước được thay đổi.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T06`
- Output `python scripts/tasks/check_output.py T06`
- Merge `bash scripts/ci/validate_merge.sh main T06`

Test nghiệm thu `tests.test_t06`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Cần văn bản bài báo và xác nhận phạm vi thí nghiệm.
