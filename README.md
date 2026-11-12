# IE212 — Khai phá luật kết hợp trên Instacart

Đề tài IE212 nghiên cứu HDFS, Spark SQL, DApriori giới hạn tập mục nhỏ, Parallel FP-Growth và so sánh Java Hadoop MapReduce với Spark trên tác vụ đếm cặp. Tình trạng triển khai và phạm vi đăng ký nằm trong [yêu cầu](docs/requirements.md) và [tiến độ](reports/progress.md).

## Kiểm tra bootstrap

Cần Python 3.11+ và Git hỗ trợ `merge-tree --write-tree` (Git 2.38+). Các lệnh Bash dùng trong Ubuntu/WSL2 hoặc Git Bash. Kiểm tra mẫu chỉ dùng thư viện chuẩn Python.

```sh
python scripts/tasks/validate_contracts.py
python scripts/tasks/check_input.py DEMO
python src/ie212_instacart/bootstrap_demo.py
python scripts/tasks/check_output.py DEMO
bash scripts/ci/run_tests.sh
bash scripts/ci/validate_merge.sh main
```

Merge gate cần commit cho feature branch và ref main. Kết quả output gate nằm trong `artifacts/quality/`.

## Cấu hình Git sau khi clone

Giữ `prompt.md` và `prompt.txt` cục bộ. Nếu dùng các tệp này, thêm hai tên vào `.git/info/exclude` của bản clone để Git bỏ qua khi stage. Bật hook bằng `git config --local core.hooksPath .githooks`. Hook kiểm tra staging trước commit và lịch sử trước push. CI kiểm lại các tệp được Git theo dõi. Phạm vi dùng chung nằm trong [yêu cầu](docs/requirements.md).

Chọn task đủ phụ thuộc trong [registry](tasks/registry.toml), xem [quy trình](docs/collaboration.md), chạy input gate, làm trên nhánh riêng rồi chạy output/merge gate. Luồng A phụ trách Data/Spark/Mining. Luồng B phụ trách Hadoop/Quality/Benchmark. Các phần dùng chung được review chéo.

Các phiên bản Spark, Java, Hadoop cho pipeline sẽ được kiểm và pin ở T07. Dữ liệu full và HDFS được thiết lập theo task tương ứng. [Kiến trúc](docs/architecture.md) · [Contract dữ liệu](docs/data_contract.md) · [Giao thức thực nghiệm](docs/experiment_protocol.md)
