# T18 — Triển khai DApriori trên Spark k≤2

P4 · Luồng A · Phạm vi M · Owner unassigned

## Mục tiêu và phạm vi

Đếm singleton, sinh/prune candidate, phân phối và reduce số đếm cặp trên Spark. Đối chiếu [yêu cầu đăng ký](../../docs/requirements.md) và [contract](task.toml).

## Đầu vào và phụ thuộc

- `docs/adr/0002-dapriori-scope.md`
- `src/ie212_instacart/preprocessing/baskets.py`
- `src/ie212_instacart/validation/oracle.py`

Trước bắt đầu cần T06, T12, T14. Trước merge cần đủ điều kiện bắt đầu và các kiểm tra tích hợp trong contract.

## Đầu ra và tiêu chí nghiệm thu

- `src/ie212_instacart/mining/dapriori.py`
- `tests/test_t18.py`

Fixture kiểm ngưỡng, tập rỗng, item trùng và độ dài k. Mapping bài báo có khác biệt được ghi rõ.

## Cổng kiểm tra và bàn giao

- Input `python scripts/tasks/check_input.py T18`
- Output `python scripts/tasks/check_output.py T18`
- Merge `bash scripts/ci/validate_merge.sh main T18`

Test nghiệm thu `tests.test_t18`. Gate báo BLOCKED nếu chưa có đầu vào, đầu ra hoặc module test. Ghi lệnh, input, expected/actual, commit và hạn chế; sau review lưu `review.toml` theo quy ước registry. Thành viên còn lại xác nhận đủ AC và smoke phù hợp trước done.

## Rủi ro và blocker

Chờ mapping Algorithm 1, basket và oracle.
