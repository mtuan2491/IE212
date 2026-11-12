# T10 — Tiếp nhận Instacart prior/full thật

P2 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Nhập đủ file được phép vào kho raw và ghi nguồn, hash, header, byte và split. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/data_contract.md`
- `scripts/data/verify_input.py`

Trước bắt đầu cần T09. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `docs/data/instacart_manifest.json`
- `scripts/data/import_instacart.py`

Đọc được prior, kiểm hash có provenance, giữ raw ngoài Git và tách train/test.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T10`
- Output `python scripts/tasks/check_output.py T10`
- Merge `bash scripts/ci/validate_merge.sh main T10`

Test nghiệm thu `tests.test_t10`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Cần xác nhận nguồn và vị trí kho raw.
