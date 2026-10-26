# Lab03 – Spark DataFrame và Spark SQL

Lab03 gồm **thực hành trên lớp** với MovieLens mini và **bài tập về nhà** phân tích dữ liệu thương mại điện tử Fecom. Hai notebook đã có code, Markdown và output; dùng PySpark 3.5.1 với `master("local[*]")`, múi giờ UTC và 8 shuffle partition.

| Nội dung | Notebook | Dữ liệu | Hướng dẫn và kết quả |
| --- | --- | --- | --- |
| Thực hành trên lớp | [Lab03_ThucHanh.ipynb](src/Lab03_ThucHanh.ipynb) | [movielens-mini/](data/movielens-mini/) | [Hướng dẫn thực hành](docs/Huong_dan_Lab3_Thuc_Hanh.md), gồm kết quả đối chiếu |
| Bài tập về nhà | [Lab03_BTVN.ipynb](src/Lab03_BTVN.ipynb) | [fecom/](data/fecom/) | [Hướng dẫn BTVN](docs/Huong_dan_Lab3_BTVN.md), [kết quả Bài 1–8](docs/result.md), [báo cáo PDF](report/BaoCao.pdf) |

## Mục tiêu và nội dung thực hành

- Tạo DataFrame từ RDD, danh sách Python và CSV; khai báo, kiểm tra lược đồ.
- Chọn, lọc, biến đổi, khử trùng và sắp xếp dữ liệu bằng DataFrame API.
- Tổng hợp bằng `groupBy().agg()`, nối bảng và xử lý giá trị NULL.
- Viết truy vấn Spark SQL, đối chiếu với DataFrame API và xem kế hoạch bằng `explain()`.
- Dùng Window để lấy top-N theo nhóm và phân biệt `row_number`, `rank`, `dense_rank`.

Notebook thực hành gồm Phần A chuẩn bị môi trường/dữ liệu và Phần B từ làm quen DataFrame đến B.6 Window. Output xác nhận 184 đánh giá, 50 phim, 50 người dùng và 15 nghề; 14 phim có đánh giá, 36 phim chưa có đánh giá. Hai cách viết DataFrame và SQL đã được đối chiếu hai chiều trong notebook.

## Bài tập về nhà – Fecom

| Bài | Nội dung | Kết quả chính từ output đã lưu |
| --- | --- | --- |
| 1 | Đọc CSV, kiểm tra lược đồ, thời gian và khóa | 5 bảng có số dòng khớp dữ liệu đi kèm |
| 2 | Đếm đơn hàng, khách đã mua và người bán | 99.441 đơn; 96.096 khách; 3.095 người bán |
| 3 | Đơn hàng theo quốc gia | 27 quốc gia; Germany dẫn đầu với 41.754 đơn |
| 4 | Đơn hàng theo năm–tháng | 25 nhóm có đơn hàng |
| 5 | Phân bố và trung bình điểm đánh giá | 99.223 đánh giá; trung bình 4,09 |
| 6 | Xếp hạng người bán bằng Window | Doanh thu dẫn đầu 249.640,70 |
| 7 | Doanh thu năm 2024 theo danh mục | 8.643.697,60; 71 nhóm danh mục, gồm `#N/A` |
| 8 | Sản phẩm bán chạy và điểm trung bình | Sản phẩm dẫn đầu có 527 lượt bán; điểm 4,02 |

Bài 1–6 bắt buộc, Bài 7–8 tự chọn; cả 8 bài đều có output. Doanh thu được notebook tính bằng **`Price + Freight_Value`**, không lọc trạng thái đơn; không gán đơn vị tiền khi dữ liệu chưa xác nhận. Phần D so sánh Hadoop MapReduce, Spark RDD và Spark DataFrame/Spark SQL nằm trong [báo cáo](report/BaoCao.pdf).

## Bộ dữ liệu

| Thư mục | File và quy mô | Cách đọc |
| --- | --- | --- |
| [fecom/](data/fecom/) | `Orders.csv`: 99.441 dòng; `Order_Items.csv`: 112.650; `Products.csv`: 32.951; `Customer_List.csv`: 102.727; `Order_Reviews.csv`: 99.223 | UTF-8, có header, phân cách `;`; reviews có trường văn bản nhiều dòng |
| [movielens-mini/](data/movielens-mini/) | `movies.txt`: 50 dòng; `ratings_1.txt`: 84; `ratings_2.txt`: 100; `users.txt`: 50; `occupation.txt`: 15 | Không header, phân cách dấu phẩy; Genres chứa nhiều thể loại phân cách `\|` |

Số bản ghi được kiểm tra trực tiếp bằng CSV parser và khớp output notebook. Bộ MovieLens mini trùng nội dung với Lab02. Chưa có tài liệu nguồn, phiên bản phát hành hoặc giấy phép riêng của Fecom và bộ mini đi kèm; không suy ra từ tên bộ dữ liệu.

## Cấu trúc thư mục

```text
Lab03/
├── README.md
├── src/
│   ├── Lab03_ThucHanh.ipynb
│   └── Lab03_BTVN.ipynb
├── data/
│   ├── fecom/
│   │   ├── Orders.csv
│   │   ├── Order_Items.csv
│   │   ├── Products.csv
│   │   ├── Customer_List.csv
│   │   └── Order_Reviews.csv
│   └── movielens-mini/
│       ├── movies.txt
│       ├── ratings_1.txt
│       ├── ratings_2.txt
│       ├── users.txt
│       └── occupation.txt
├── docs/
│   ├── Huong_dan_Lab3_Thuc_Hanh.md
│   ├── Huong_dan_Lab3_BTVN.md
│   └── result.md
└── report/
    └── BaoCao.pdf
```

Giữ tên notebook và vị trí `docs/result.md` theo quy ước Lab02. Các bản tên `_new` hoặc `_HoanChinh(1)` không có trong thư mục được cung cấp; hai file hiện có đã lưu output đầy đủ nên được giữ nguyên.

## Chạy nhanh

1. Tải notebook cần dùng và toàn bộ thư mục `data/` của Lab03 về máy.
2. Mở PowerShell tại `Lab03/`, chạy `Compress-Archive -LiteralPath .\data -DestinationPath .\data.zip`. ZIP phải có tiền tố `data/`, chứa cả `fecom/` và `movielens-mini/`.
3. Mở notebook trên Google Colab, kết nối runtime Python rồi chạy từ cell cài PySpark xuống dưới. Khi cell upload đầu tiên hỏi file, chọn đúng tên **`data.zip`**.
4. Kiểm tra `PySpark: 3.5.1`, danh sách dữ liệu và chạy tiếp theo thứ tự: thực hành A → B.6 → dọn dẹp; BTVN A → Bài 1–8.
5. Đối chiếu output theo [hướng dẫn thực hành](docs/Huong_dan_Lab3_Thuc_Hanh.md) hoặc [kết quả BTVN](docs/result.md), rồi tải `.ipynb` có output về máy.

**Lưu ý:** cả hai notebook có cell upload `data.zip` chung ở đầu, kiểm tra cả hai bộ dữ liệu. Cell `prepare_data` phía sau có thể nhận file lẻ/ZIP nhưng không thay thế yêu cầu của cell đầu khi chạy nguyên notebook trên runtime mới. Log pip đã lưu có xung đột `dataproc-spark-connect` với PySpark 3.5.1; các cell sau vẫn in đúng phiên bản và có kết quả. Xem hướng dẫn tương ứng để xử lý.

## Kết quả và báo cáo

[Kết quả Bài 1–8](docs/result.md) ghi rõ cách đếm khách đã mua, doanh thu gồm phí vận chuyển và cách gộp đánh giá theo đơn trước khi nối bảng. [Báo cáo đầy đủ](report/BaoCao.pdf) chứa phần trình bày và so sánh ở Phần D.

Các CSV lớn nhất khoảng 12,84–16,03 MB, đều dưới 100 MiB; giữ dữ liệu trong Git thông thường. `data.zip` chỉ dùng để upload, đã được loại khỏi Git bằng `.gitignore`.
