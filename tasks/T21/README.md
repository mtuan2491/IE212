# T21 — Viết Spark pair count tương đương

P4 · Luồng B · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Spark đọc cùng định dạng input, chuẩn hóa A<B và đếm mỗi pair một lần mỗi order. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/data_contract.md`
- `tests/fixtures/instacart/orders.csv`

Trước bắt đầu cần T09. Trước merge cần T13 cùng dependency bắt đầu.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/mining/pair_count.py`
- `tests/test_t21.py`

Đầu ra theo cùng schema và kiểm toàn bộ fixture. Chạy HDFS theo handoff T13.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T21`
- Output `python scripts/tasks/check_output.py T21`
- Merge `bash scripts/ci/validate_merge.sh main T21`

Test nghiệm thu `tests.test_t21`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Có thể làm fixture trước. Nghiệm thu HDFS chờ T13.
