# T28 — Viết báo cáo phương pháp và thực nghiệm

P6 · Luồng Chung · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Tóm tắt paper, phương pháp, thực nghiệm, giới hạn, kết quả và nguồn. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/research.md`
- `reports/results.md`

Trước bắt đầu cần T06, T26. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `reports/final_report.md`
- `presentation/outline.md`

Truy vết biểu đồ về run IDs và câu chữ về scope đã kiểm chứng.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T28`
- Output `python scripts/tasks/check_output.py T28`
- Merge `bash scripts/ci/validate_merge.sh main T28`

Test nghiệm thu `tests.test_t28`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ nguồn học thuật và kết quả thực nghiệm.
