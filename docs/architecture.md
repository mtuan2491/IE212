# Kiến trúc dự kiến

1. Ingestion xác minh provenance, schema và chất lượng dữ liệu, lưu raw theo namespace HDFS đã duyệt.
2. Spark SQL/DataFrame join và chuẩn hóa basket theo order_id, lưu Parquet và kiểm round trip.
3. DApriori và FP-Growth dùng basket đã kiểm; tầng validation có oracle, rules và parity từng khóa.
4. Java MapReduce và Spark pair count đọc cùng input contract. Output pair được chuẩn hóa trước khi benchmark.
5. Benchmark lưu metadata, kết quả thô và báo cáo theo từng trục. Lịch sử và raw legacy nằm ngoài repo mới.

`tasks/` chứa contract TOML và dependency graph. `issues/` chứa bản local. `scripts/tasks` đọc contract bằng thư viện chuẩn. Gate merge kiểm cây hợp nhất trong thư mục tạm. Mẫu IE307 được điều chỉnh thành review chéo và kiểm offline cho giai đoạn chưa có GitHub Project.

Chỉ đưa vào scaffold file có chức năng hoặc tài liệu sử dụng được. Package Hadoop Java và mô-đun Spark sẽ xuất hiện khi đến các task đã đăng ký. [ADR bootstrap](adr/0001-offline-bootstrap-gates.md)
