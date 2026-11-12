# T13 — Lưu Parquet và xác minh HDFS round trip

P2 · Luồng A+B · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Lưu và đọc Parquet theo URI HDFS, so schema và toàn bộ basket của fixture. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/runbooks/hdfs.md`
- `src/ie212_instacart/preprocessing/baskets.py`

Trước bắt đầu cần T08, T12. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/preprocessing/storage.py`
- `docs/runbooks/hdfs_pipeline.md`

Ghi evidence HDFS thật, đếm row/key và hash chuẩn hóa trước/sau.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T13`
- Output `python scripts/tasks/check_output.py T13`
- Merge `bash scripts/ci/validate_merge.sh main T13`

Test nghiệm thu `tests.test_t13`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Cần HDFS và pipeline basket đã review.
