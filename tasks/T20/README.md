# T20 — Viết Java Hadoop MapReduce đếm cặp

P4 · Luồng B · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Java Hadoop Mapper/Reducer dùng cùng định dạng basket và xuất product_a/product_b/count. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/runbooks/runtime.md`
- `docs/data_contract.md`

Trước bắt đầu cần T07, T09. Trước merge cần T13 cùng dependency bắt đầu.

## Đầu ra và tiêu chí nghiệm thu

- `mapreduce/pom.xml`
- `mapreduce/src/main/java/ie212/PairCount.java`
- `tests/test_t20.py`

JUnit fixture gồm dedup, A<B, basket nhỏ và khóa trùng; kiểm HDFS sau T13.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T20`
- Output `python scripts/tasks/check_output.py T20`
- Merge `bash scripts/ci/validate_merge.sh main T20`

Test nghiệm thu `tests.test_t20`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Có thể làm phần fixture trước. Nghiệm thu HDFS chờ T13.
