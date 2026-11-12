# T29 — Kiểm release từ clone sạch

P6 · Luồng Chung · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Chạy demo, kiểm reproducibility, tài liệu cài đặt và presentation. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/runbooks/demo.md`
- `reports/final_report.md`
- `presentation/outline.md`

Trước bắt đầu cần T27, T28. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/runbooks/release.md`
- `reports/release_checks.md`

Ghi SHA, lệnh, expected/actual, trạng thái môi trường và review chéo.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T29`
- Output `python scripts/tasks/check_output.py T29`
- Merge `bash scripts/ci/validate_merge.sh main T29`

Test nghiệm thu `tests.test_t29`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ demo, báo cáo và môi trường nghiệm thu.
