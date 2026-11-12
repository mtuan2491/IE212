# T27 — Đóng gói demo và runbook full

P6 · Luồng A · Phạm vi S · Owner unassigned

## Mục tiêu và phạm vi

Từ clone sạch chạy CLI fixture, rồi tài liệu hóa tuyến full/HDFS. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/validation/fpgrowth.md`
- `src/ie212_instacart/validation/itemset_parity.py`
- `src/ie212_instacart/validation/pair_parity.py`

Trước bắt đầu cần T17, T19, T22. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `scripts/demo.py`
- `docs/runbooks/demo.md`

Ghi expected output cho fixture và cách chẩn đoán nếu môi trường full thiếu.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T27`
- Output `python scripts/tasks/check_output.py T27`
- Merge `bash scripts/ci/validate_merge.sh main T27`

Test nghiệm thu `tests.test_t27`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ cả ba phép kiểm độ đúng.
