# Hướng dẫn Lab03 – Thực hành Spark DataFrame và Spark SQL

Tài liệu môn **IE212 – Công nghệ dữ liệu lớn**, dành cho [Lab03_ThucHanh.ipynb](../src/Lab03_ThucHanh.ipynb). Mục tiêu là chuyển từ cách xử lý RDD của Lab02 sang DataFrame có lược đồ, thực hiện tổng hợp, nối bảng, Spark SQL và Window trên MovieLens mini.

Phần BTVN Fecom có [notebook](../src/Lab03_BTVN.ipynb), [hướng dẫn](Huong_dan_Lab3_BTVN.md) và [kết quả](result.md) riêng.

## Mục lục

- [1. Nội dung notebook](#1-nội-dung-notebook)
- [2. Cấu trúc dữ liệu](#2-cấu-trúc-dữ-liệu)
- [3. Chạy trên Google Colab](#3-chạy-trên-google-colab)
- [4. Chạy trên máy cá nhân](#4-chạy-trên-máy-cá-nhân)
- [5. Kết quả mong đợi](#5-kết-quả-mong-đợi)
- [6. Lỗi thường gặp](#6-lỗi-thường-gặp)
- [7. Lưu kết quả](#7-lưu-kết-quả)

## 1. Nội dung notebook

Notebook có 31 cell code, đều đã lưu output; các câu hỏi kiểm tra nhanh đã có phần trả lời. Chạy Phần A → làm quen DataFrame → B.1–B.6 → dọn dẹp.

| Phần | Thao tác thực sự có trong code |
| --- | --- |
| A – Chuẩn bị | Cài PySpark 3.5.1; upload dữ liệu; chọn/cài Java 17; tạo Spark `local[*]`, UTC, 8 shuffle partition; dựng RDD ratings |
| Làm quen | `ratings.toDF()`, `createDataFrame()` từ danh sách Python |
| B.1 – Lược đồ | Đọc CSV không header bằng DDL/StructType; `printSchema`, `show`, `count`; minh họa đọc sai `header=True` |
| B.2 – Hàm cơ bản | `select`, `filter`/`where`, `withColumn`, đổi tên/kiểu cột, hàm chuỗi/mảng, `distinct`, `dropDuplicates`, `sort` |
| B.3 – Tổng hợp | `groupBy().agg()` với count/avg/min/max; `collect_set`, `countDistinct`; nối tên phim, tìm phim cao điểm với ít nhất 5 lượt |
| B.4 – Join | Thực thi `inner`, `left`, `left_anti` trên phim và bảng điểm; quan sát NULL ở phim chưa có đánh giá |
| B.5 – Spark SQL | Tạo temp view, truy vấn SQL tương ứng; kiểm tra `exceptAll` hai chiều và xem `explain()` |
| B.6 – Window | `explode(split(...))`; top-2 phim theo thể loại bằng `row_number`; so `row_number`, `rank`, `dense_rank` |
| Dọn dẹp | `spark.stop()` và in thông báo đóng SparkSession |

Các kiểu join khác và `lag`/`lead` được giới thiệu trong Markdown, chưa được thực thi thành bài giải trong notebook.

## 2. Cấu trúc dữ liệu

Năm file ở [data/movielens-mini/](../data/movielens-mini/) là văn bản phân cách bằng dấu phẩy, **không có header**, trùng nội dung bộ mini của Lab02.

| File | Dòng | Lược đồ trong notebook |
| --- | ---: | --- |
| [movies.txt](../data/movielens-mini/movies.txt) | 50 | `MovieID INT, Title STRING, Genres STRING` |
| [ratings_1.txt](../data/movielens-mini/ratings_1.txt) | 84 | `UserID INT, MovieID INT, Rating DOUBLE, Timestamp BIGINT` |
| [ratings_2.txt](../data/movielens-mini/ratings_2.txt) | 100 | Cùng lược đồ ratings_1; được đọc chung bằng danh sách hai đường dẫn |
| [users.txt](../data/movielens-mini/users.txt) | 50 | `UserID INT, Gender STRING, Age INT, Occupation INT, Zip STRING` |
| [occupation.txt](../data/movielens-mini/occupation.txt) | 15 | `OccID INT, Occupation STRING` |

Genres chứa nhiều thể loại phân cách bằng ký tự `|`. Trong hàm Spark `split`, dùng regex `r"\|"` hoặc `"\\|"`. Rating là số thực, không ép sang INT. Bảng users/occupation được đọc và kiểm tra quy mô; các bài tổng hợp, SQL và Window chính dùng movies/ratings.

## 3. Chạy trên Google Colab

### Bước 1. Chuẩn bị notebook và ZIP

Tải [notebook thực hành](../src/Lab03_ThucHanh.ipynb) và toàn bộ `Lab03/data/`, gồm **cả MovieLens và Fecom**. Mở PowerShell tại `Lab03/`:

```powershell
Compress-Archive -LiteralPath .\data -DestinationPath .\data.zip
```

ZIP cần chứa `data/movielens-mini/` với đủ 5 file và `data/fecom/` với đủ 5 CSV. Nếu ZIP cũ tồn tại, chuyển bản đó sang nơi khác trước khi tạo lại.

Notebook thực hành có cell upload chung ngay sau cài PySpark: kiểm tra `movies.txt` và `Orders.csv`, mở **`uploaded["data.zip"]`**, giải nén vào `/content/`, rồi liệt kê cả hai thư mục. Vì vậy, dù mô tả đầu notebook cho phép 5 file lẻ, **chạy nguyên notebook trên runtime mới phải dùng ZIP đủ hai bộ**. Cell `prepare_data` phía sau hỗ trợ file lẻ hoặc ZIP nhưng chỉ được chạy sau cell chung này.

### Bước 2. Mở notebook và cài PySpark

Mở notebook trên Google Colab, kết nối runtime Python. Chạy `%pip install -q pyspark==3.5.1`. Giữ phiên bản này để assertion trong cell tạo Spark đạt yêu cầu. Notebook không in phiên bản Python hoặc `java -version` của runtime gốc.

Log pip đã lưu có thông báo xung đột `dataproc-spark-connect 1.1.0` cần PySpark 4.0. Các cell sau vẫn in `PySpark: 3.5.1` và chạy tới cell dọn dẹp; thông báo resolver không đồng nghĩa toàn bộ notebook thất bại. Nếu đã import phiên bản PySpark khác, khởi động lại runtime rồi chạy từ đầu.

### Bước 3. Upload và kiểm tra đường dẫn

Giữ cwd `/content`. Chạy cell upload chung, chọn đúng tên **`data.zip`**. Cần thấy danh sách MovieLens/Fecom và các đường dẫn `/content/data/movielens-mini`, `/content/data/fecom`.

Sau đó chạy cell Java/Spark, kiểm tra `PySpark: 3.5.1`. Cell này chọn Java 17 từ `/usr/lib/jvm` hoặc cài `openjdk-17-jre-headless` nếu thiếu.

Tiếp tục cell `prepare_data`: kiểm tra đủ 5 file MovieLens không rỗng, chỉ upload bổ sung nếu thiếu. Đường dẫn đọc chính là `ML = "/content/data/movielens-mini"`.

### Bước 4. Chạy từ A đến B.6

Chạy các cell theo thứ tự: tạo RDD ratings → tạo DataFrame → B.1 đến B.6. B.4 dùng `tb` từ B.3; B.5 dùng `ket_qua_df`; B.6 dùng lại bảng điểm và danh mục phim. Không bỏ qua các cell tạo biến.

Có thể dùng **Run all** từ đầu, chọn ZIP khi được hỏi. Hai cell minh họa đọc sai header và tách sai Genres vẫn chạy được và có output sai có chủ đích, kèm cell giải thích/sửa ngay sau đó. Không sửa output các cell này thành kết quả đúng.

### Bước 5. Đối chiếu và kết thúc

Kiểm tra các mốc ở phần 5 rồi chạy cell dọn dẹp `spark.stop()`. Muốn tính tiếp sau khi đóng Spark, tạo lại Spark và các bảng phụ thuộc hoặc chạy lại từ đầu. Tải notebook có output sau khi hoàn tất.

## 4. Chạy trên máy cá nhân

Chưa có lượt chạy local được ghi nhận. Dùng một **bản sao** notebook, chuẩn bị PySpark 3.5.1 và JDK 17, chọn đúng kernel. Bỏ qua cell upload chung có `google.colab`; thay đoạn tự dò/cài Java của Colab bằng Java đã cấu hình trên máy.

Tại cell `prepare_data`, đặt `ML = "../data/movielens-mini"` khi cwd là `Lab03/src/`; nếu cwd là gốc repository, dùng `ML = "Lab03/data/movielens-mini"`. Cần đủ 5 file trước khi gọi hàm để không mở upload Colab. `FE` không được dùng trong các phép phân tích thực hành nên không cần đặt lại sau khi bỏ cell upload chung. Giữ nguyên code B.1–B.6 trong bản gốc repository.

## 5. Kết quả mong đợi

Các mốc lấy trực tiếp từ output đã lưu, không phải lượt chạy mới trong quá trình soạn tài liệu.

| Vị trí | Kết quả đối chiếu |
| --- | --- |
| A – Spark | `PySpark: 3.5.1`; RDD ratings có 184 bản ghi |
| B.1 – Đọc đủ dữ liệu | movies 50; ratings 184; users 50; occupation 15 |
| B.1 – Sai header có chủ đích | ratings_1 còn 83 dòng; tên cột là `['7', '1020', '4.5', '1577836800']` |
| B.1 – Hai lược đồ | So sánh StructType với DDL ra `True` |
| B.2 – Lọc | MovieID 1020, Rating từ 4,0 có 6 lượt |
| B.2 – Genres | Tách sai cho The Godfather ra 12 phần; tách đúng ra 2 thể loại |
| B.2 – Khử trùng | 49 UserID, 14 MovieID được đánh giá; `distinct()` toàn bộ ratings vẫn 184 dòng |
| B.3 – Tổng hợp | 14 phim; tổng 184 lượt; Sunset Boulevard (1950) cao nhất với 4,36/7 lượt khi yêu cầu ít nhất 5 lượt |
| B.4 – Join | inner 14; left 50; left_anti 36; phim không có đánh giá mang NULL |
| B.5 – SQL | 14 dòng, phép `exceptAll` in 0; cả hai assertion so sánh hai chiều không dừng |
| B.5 – Kế hoạch | Cả hai có HashAggregate, Exchange và BroadcastHashJoin; vị trí aggregate/khóa nhóm khác nhau |
| B.6 – Trải thể loại | 122 cặp phim–thể loại |
| B.6 – Top-2 | 20 dòng trong 12 thể loại có đánh giá; Family, Film-Noir, Horror, Mystery chỉ có một phim có đánh giá |
| B.6 – Đồng điểm | Hai phim điểm 4,0 có `rank=3`, `dense_rank=3`; phim kế điểm 3,89 có `rank=5`, `dense_rank=4` |
| Dọn dẹp | `Đã đóng SparkSession.` |

SQL nhóm theo Title, DataFrame nhóm theo MovieID trước khi nối tên. Hai kết quả khớp trên bộ dữ liệu này; không suy ra sẽ luôn khớp nếu nhiều mã phim dùng chung Title. Các kế hoạch đã lưu cũng không hoàn toàn giống nhau. Window không có khóa phụ có thể đổi thứ tự giữa các phim đồng điểm.

## 6. Lỗi thường gặp

| Hiện tượng | Cách kiểm tra và xử lý |
| --- | --- |
| `KeyError: 'data.zip'` | Cell chung chỉ mở tên `data.zip`; dùng ZIP đủ hai bộ và có tiền tố `data/` |
| Không tìm thấy Fecom khi chỉ học MovieLens | Cell chung vẫn kiểm tra/liệt kê Fecom; dùng cấu trúc ZIP ở bước 1 |
| Thiếu dữ liệu hoặc `PATH_NOT_FOUND` | Kiểm tra `ML`, cwd và đủ 5 file; dùng `prepare_data` để upload bổ sung |
| Assertion số dòng không đạt | Kiểm tra đúng bộ mini, `header=False` và lược đồ; không áp kết quả 83 dòng của cell sai header cho DataFrame chính |
| Genres bị tách thành từng ký tự | Dùng regex `r"\|"` hoặc `"\\|"`; cell sai `"|"` được giữ để minh họa |
| `Column` không dùng được với `and`/`or` | Dùng `&`/`|` và bọc từng điều kiện trong ngoặc như cell B.2 |
| `NameError` với `tb`, `ket_qua_df`, `df_the_loai` | Chạy các phần trước theo đúng thứ tự; reset runtime làm mất mọi biến |
| Spark khác 3.5.1 hoặc Java gateway lỗi | Kiểm tra log cài đặt/Java và assertion phiên bản; khởi động lại runtime sau khi đổi phiên bản đã import |
| Không chạy tiếp được sau dọn dẹp | Tạo lại Spark và DataFrame phụ thuộc; `spark.stop()` đã đóng phiên |

## 7. Lưu kết quả

Tải `.ipynb` có output về máy sau khi chạy xong, mở lại để kiểm tra đủ 31 cell code có output và thông báo đóng Spark. Không dùng **Clear all outputs**. Bản lưu hiện không có output loại `error`, nhưng còn log xung đột phụ thuộc của pip như phần 3.

Giữ notebook gốc khi thử thay đổi môi trường/local trên bản sao. Không thêm `data.zip`, môi trường ảo hoặc checkpoint vào Git. Kết quả BTVN và so sánh Phần D xem [result.md](result.md) và [báo cáo](../report/BaoCao.pdf).
