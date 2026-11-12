# Yêu cầu đăng ký và truy vết

**Đề tài.** Xây dựng hệ thống khai phá luật kết hợp và đánh giá hiệu suất trên dữ liệu mua sắm Instacart.

Phạm vi dưới đây được truy vết từ mục 1 của đặc tả khởi tạo lưu cục bộ. Dùng tài liệu này làm nguồn yêu cầu trong bản clone. Các kiểm chứng dưới đây là kế hoạch của project mới.

| Phạm vi | Task và bằng chứng cần có |
| --- | --- |
| Nguồn Instacart theo đăng ký, dataset prior/full và các bảng đơn hàng, sản phẩm, ngành hàng, khu vực | T09–T11. Manifest nguồn/hash/schema và quality report từng split. |
| Lưu HDFS, Spark SQL/DataFrame chuẩn hóa giao dịch theo order_id | T08, T12, T13. Assertions khóa, dedup, đủ basket và round trip với HDFS URI. |
| Parallel FP-Growth Spark MLlib | T14, T15, T17. Oracle nhỏ và parity từng khóa/tần suất. |
| DApriori Spark giới hạn tập mục nhỏ | T06, T18, T19. Mapping với bài báo, k công bố, parity cùng input/ngưỡng. |
| Support, Confidence, Lift | T14, T16, T17. Kiểm riêng các count và luật trên fixture. |
| Java Hadoop MapReduce so với Spark trên cùng tác vụ đếm cặp | T20–T22. Cùng đầu vào, schema output, phạm vi và parity đầy đủ. |
| Nhiều quy mô/ngưỡng/cấu hình và khả năng mở rộng | T23–T26. Manifest tập, metadata, repeats, số đo và giới hạn. |
| Demo, báo cáo, biểu đồ và quy trình tái lập | T27–T29. Clean clone, smoke, runbooks và evidence. |
| Phối hợp hai người và tự động hóa kiểm thử | T01–T05. Bảo toàn repo cũ, contract, gates, CI nhẹ và review chéo. |

## Nguồn đã đăng ký

- Fernandez-Basso, Ruiz và Martin-Bautista (2024), *New Spark Solutions for Distributed Frequent Itemset and Association Rule Mining Algorithms*, Cluster Computing. [DOI](https://doi.org/10.1007/s10586-023-04014-w)
- Spark MLlib, [FP-Growth](https://spark.apache.org/docs/latest/ml-frequent-pattern-mining.html). Pin tài liệu theo runtime sau T07.
- [Instacart Market Basket Analysis](https://zenodo.org/records/2654444). T09/T10 xác minh metadata và checksum được công bố nếu có.
