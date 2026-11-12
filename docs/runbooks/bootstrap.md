# Runbook kiểm bootstrap

Cần Python 3.11+ và Git 2.38+. Windows có thể chạy entry point Python trực tiếp. Bash scripts chạy trong Ubuntu/WSL2 hoặc Git Bash. Xem `make doctor` để kiểm công cụ đang có.

Chạy `make task-input TASK=DEMO`, tạo fixture output bằng `python src/ie212_instacart/bootstrap_demo.py` rồi chạy `make task-output TASK=DEMO`. Kiểm `artifacts/quality/DEMO/output.json` và so cặp (3,7)=2, (3,9)=1. Chạy `make test` cho suite bootstrap. Merge gate cần cả base và HEAD đã commit.

Khi lệnh HDFS hoặc dataset full chưa sẵn sàng, ghi BLOCKED và chuyển sang kiểm fixture theo đúng phạm vi. T07/T08 sẽ bổ sung cài đặt phiên bản cụ thể và thao tác trên namespace HDFS đã được duyệt.
