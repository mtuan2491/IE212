# T11 — Profile và audit các bảng CSV

P2 · Luồng A · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Kiểm schema, null hợp lệ, duplicate, invalid, orphan và report theo split. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/data_contract.md`
- `tests/fixtures/instacart/orders.csv`

Trước bắt đầu cần T09. Trước merge cần T10 cùng dependency bắt đầu.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/ingestion/profile.py`
- `docs/data/quality_summary.md`

Fixture có ca âm. Bản chạy full tham chiếu manifest T10 và ghi số hàng theo lý do.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T11`
- Output `python scripts/tasks/check_output.py T11`
- Merge `bash scripts/ci/validate_merge.sh main T11`

Test nghiệm thu `tests.test_t11`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Fixture có thể bắt đầu sau T09, đối chiếu full chờ T10.
