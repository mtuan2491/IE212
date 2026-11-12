# Làm việc nhóm hai người

- A phụ trách data, Spark SQL và mining. B phụ trách Hadoop, CI và benchmark. Cả hai review contract, thực nghiệm và báo cáo. Thống nhất file dùng chung trước khi triển khai song song.
- Chọn một task và xác nhận owner. Chạy input gate trước code. Tạo nhánh feat/Txx-… hoặc fix/Txx-… từ base đã biết. Commit và PR theo phạm vi task.
- Sau sửa chạy output gate rồi merge gate trên revision định gửi. Reviewer còn lại đối chiếu AC, evidence và revision. Sau merge chạy smoke thích hợp, ghi SHA và review trước khi cập nhật done.
- Khi conflict, đồng bộ trên nhánh task hoặc tạo nhánh sửa riêng. Chạy lại cả hai gate và review trên revision mới. Khi cần hoàn tác một thay đổi đã merge, tạo PR revert và chạy gate.
- Bản issue local dùng ID Txx cố định. Branch protection và required checks được chốt khi nhóm có remote và quyền.
