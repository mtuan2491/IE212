# Cấu hình mẫu

`storage.raw` và `storage.processed` là đường dẫn tương đối tính từ repo. `hdfs_uri` và `hdfs_project_path` chỉ có hiệu lực sau kiểm HDFS ở T08. Không ghi credential trong cấu hình.

`experiment.seed` là số nguyên. Support nằm trong (0,1], confidence trong [0,1]. Phạm vi khởi điểm `max_itemset_size=2`. Ghi cấu hình từng lần chạy và lặp ít nhất ba lần khi khả thi. T07 pin môi trường và T24 triển khai đọc cấu hình.
