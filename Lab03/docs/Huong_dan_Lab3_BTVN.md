# Hướng dẫn Lab03 – Bài tập về nhà Fecom

Tài liệu dành cho [Lab03_BTVN.ipynb](../src/Lab03_BTVN.ipynb), dùng Spark DataFrame để đọc, kiểm tra, nối và tổng hợp dữ liệu Fecom; dùng Window để xếp hạng người bán. Bài 1–6 bắt buộc, Bài 7–8 tự chọn. Phần D nằm trong [báo cáo PDF](../report/BaoCao.pdf).

## Mục lục

- [1. Chuẩn bị](#1-chuẩn-bị)
- [2. Chạy trên Google Colab](#2-chạy-trên-google-colab)
- [3. Nội dung Bài 1–8](#3-nội-dung-bài-18)
- [4. Lưu ý khi xử lý dữ liệu](#4-lưu-ý-khi-xử-lý-dữ-liệu)
- [5. Chạy trên máy cá nhân](#5-chạy-trên-máy-cá-nhân)
- [6. Xử lý lỗi thường gặp](#6-xử-lý-lỗi-thường-gặp)
- [7. Kiểm tra và lưu kết quả](#7-kiểm-tra-và-lưu-kết-quả)

## 1. Chuẩn bị

- Runtime Python trên Google Colab; không có cấu hình yêu cầu GPU hoặc cụm Hadoop riêng.
- Notebook cài `pyspark==3.5.1`, chọn/cài Java 17 trên Colab rồi tạo `SparkSession` tên `IE212-Lab3-BTVN`, `local[*]`, UTC, 8 shuffle partition.
- Output xác nhận Spark `3.5.1`; chưa có output xác nhận phiên bản Python và `java -version` của lần chạy gốc.
- Tải [notebook](../src/Lab03_BTVN.ipynb), [Fecom](../data/fecom/) và [MovieLens mini](../data/movielens-mini/). Phần tính toán BTVN chỉ dùng Fecom, nhưng cell upload đầu kiểm tra và liệt kê cả hai thư mục.

### Năm file Fecom

CSV dùng UTF-8, có dòng tiêu đề và dấu phân cách **`;`**. Số dòng dưới đây là số bản ghi dữ liệu, không tính header; file reviews có nội dung xuống dòng trong trường được đặt trong dấu nháy kép.

| File | Bản ghi | Cột | Vai trò |
| --- | ---: | ---: | --- |
| [Orders.csv](../data/fecom/Orders.csv) | 99.441 | 8 | Mã đơn, khóa giao dịch khách, trạng thái và các mốc thời gian |
| [Order_Items.csv](../data/fecom/Order_Items.csv) | 112.650 | 7 | Dòng hàng của đơn: sản phẩm, người bán, giá và phí vận chuyển |
| [Products.csv](../data/fecom/Products.csv) | 32.951 | 6 | Mã sản phẩm, danh mục và kích thước/khối lượng |
| [Customer_List.csv](../data/fecom/Customer_List.csv) | 102.727 | 10 | Khóa giao dịch, mã người đăng ký, thời gian đăng ký/mua, thông tin quốc gia và nhân khẩu học |
| [Order_Reviews.csv](../data/fecom/Order_Reviews.csv) | 99.223 | 7 | Mã đánh giá, mã đơn, điểm, nội dung và thời gian đánh giá |

## 2. Chạy trên Google Colab

### Bước 1. Chuẩn bị ZIP đúng cấu trúc

Giữ toàn bộ `Lab03/data/`. Mở PowerShell tại **`Lab03/`**, chạy:

```powershell
Compress-Archive -LiteralPath .\data -DestinationPath .\data.zip
```

Nếu ZIP đã tồn tại, chuyển bản cũ sang nơi khác trước khi tạo lại. Mở ZIP, kiểm tra có `data/fecom/Orders.csv` và `data/movielens-mini/movies.txt`, cùng 8 file còn lại. ZIP chứa `Lab03/data/` hoặc chỉ chứa các CSV ở gốc không đáp ứng cell giải nén đầu tiên.

Sau giải nén, runtime cần có:

```text
/content/data/
├── fecom/
│   ├── Orders.csv
│   ├── Order_Items.csv
│   ├── Products.csv
│   ├── Customer_List.csv
│   └── Order_Reviews.csv
└── movielens-mini/
    ├── movies.txt
    ├── ratings_1.txt
    ├── ratings_2.txt
    ├── users.txt
    └── occupation.txt
```

### Bước 2. Mở notebook và cài môi trường

Mở bản tải về trên Google Colab, kết nối runtime Python và giữ thư mục làm việc `/content`. Chạy cell `%pip install -q pyspark==3.5.1` đầu tiên. Nếu runtime đã import một phiên bản PySpark khác, khởi động lại runtime rồi chạy từ đầu.

Log đã lưu có thông báo resolver: `dataproc-spark-connect 1.1.0` cần PySpark 4.0 trong khi notebook cài 3.5.1. Các cell sau vẫn in `PySpark: 3.5.1` và có kết quả. Đọc riêng traceback nếu cell dừng; không đổi sang Spark 4.x chỉ để bỏ thông báo này.

### Bước 3. Upload dữ liệu

Chạy cell ngay sau cài đặt. Nếu thiếu MovieLens `movies.txt` **hoặc** Fecom `Orders.csv`, cell gọi `files.upload()` và mở khóa `uploaded["data.zip"]`. Chọn file đúng tên **`data.zip`** đã tạo ở bước 1. Cell giải nén vào `/content/`, liệt kê cả hai bộ và đặt `ML`, `FE`.

Cell này chỉ dùng hai file đại diện để quyết định có upload, không kiểm tra đủ 10 file. Nếu runtime còn dữ liệu cũ, dùng runtime mới hoặc đối chiếu đủ file trước khi chạy tiếp.

### Bước 4. Tạo Spark và kiểm tra Fecom

Chạy cell thiết lập Java/Spark, xác nhận `PySpark: 3.5.1` và assertion không dừng. Sau đó chạy A.2: hàm `prepare_data` kiểm tra đủ 5 CSV không rỗng tại `/content/data/fecom`. Nếu thiếu, hàm cho upload file lẻ hoặc ZIP và chỉ đưa các tên cần dùng về đúng thư mục.

Khả năng nhận file lẻ của A.2 chỉ là bước bổ sung; khi chạy nguyên notebook từ đầu, cell upload chung ở bước 3 vẫn yêu cầu ZIP đúng cấu trúc nếu chưa có dữ liệu.

### Bước 5. Chạy Bài 1–8 theo thứ tự

Chạy cả hai cell của Bài 1 để tạo bảng, chuẩn hóa thời gian, kiểm tra khóa và tạo `customer_lookup`. Tiếp tục Bài 2–6 rồi Bài 7–8. Bài 7 dùng `items_money` từ Bài 6; Bài 8 dùng các bảng đã tạo ở Bài 1.

Có thể dùng **Run all** từ đầu; notebook sẽ chờ chọn ZIP nếu thiếu dữ liệu. Bản gốc BTVN kết thúc ở Bài 8, không có cell `spark.stop()` hoặc nội dung Phần D.

## 3. Nội dung Bài 1–8

| Bài | Chức năng thực tế | Mốc đối chiếu |
| --- | --- | --- |
| 1 | Đọc 5 bảng, `printSchema`, đếm dòng, kiểm tra cột, chuẩn hóa timestamp và kiểm tra tính duy nhất của khóa | Số dòng khớp bảng ở phần 1 |
| 2 | Đếm đơn; `left_semi` lấy khách có giao dịch rồi đếm `Subscriber_ID` phân biệt; đếm `Seller_ID` | 99.441; 96.096; 3.095 |
| 3 | Nối Orders với khách theo `Customer_Trx_ID`, kiểm tra không nhân dòng, gộp theo quốc gia | 27 quốc gia; Germany 41.754 đơn |
| 4 | Lấy năm, tháng từ thời điểm mua, gộp và sắp năm tăng/tháng giảm | 25 nhóm; tổng 99.441 đơn |
| 5 | Kiểm tra NULL/điểm ngoài 1–5; phân bố điểm và trung bình | 99.223 điểm hợp lệ; trung bình 4,09 |
| 6 | Chuyển tiền sang decimal, cộng giá và phí vận chuyển, tổng hợp người bán và dùng `rank()` | 3.095 người bán; dẫn đầu 249.640,70 |
| 7 | Lọc năm mua 2024, nối dòng hàng với sản phẩm, cộng doanh thu theo danh mục | 61.416 dòng hàng; 71 nhóm; 8.643.697,60 |
| 8 | Gộp đánh giá theo đơn trước khi nối dòng hàng, đếm lượt bán và tính điểm theo sản phẩm | Sản phẩm dẫn đầu 527 lượt; điểm 4,02 |

Xem bảng chi tiết và cách hiểu số liệu trong [result.md](result.md).

## 4. Lưu ý khi xử lý dữ liệu

- **CSV:** giữ `sep=";"`, `header=True`, `inferSchema=True`, UTF-8 và `mode="FAILFAST"`. Riêng reviews dùng `multiLine=True`, `escape='"'`. Notebook bỏ BOM và khoảng trắng ở tên cột. Không đếm reviews bằng số dòng văn bản hoặc tự bỏ bản ghi khi lệch số lượng.
- **Thời gian:** output hiện có cho thấy Spark suy ra timestamp cho Orders/Items/Reviews và date cho Customer_List. Cell tiếp theo đổi các mốc về timestamp; chỉ dùng mẫu `yyyy-MM-dd` hoặc `yyyy-MM-dd HH:mm` khi cột còn là string. Hai bảng kiểm tra cột string/lỗi parse trong bản lưu rỗng vì không có cột thời gian dạng string cần parse lại.
- **Khách hàng:** `Customer_Trx_ID` dùng nối đơn với thông tin giao dịch; `Subscriber_ID` dùng đếm người mua phân biệt. Có 3.286 dòng đăng ký chưa có khóa giao dịch; không coi 102.727 dòng Customer_List là số khách đã mua.
- **Khóa nối:** Orders và Products được kiểm tra duy nhất theo mã; bảng tra khách chỉ giữ `Customer_Trx_ID` không NULL và kiểm tra không trùng. So sánh số dòng trước/sau nối để tránh nhân doanh thu hoặc lượt bán.
- **Doanh thu:** Bài 6–7 cộng `Price + Freight_Value` với `decimal(20,2)`, không lọc `Order_Status`. Bài 7 chọn năm theo `Order_Purchase_Timestamp`, giữ cả nhóm danh mục `#N/A`.
- **Đánh giá:** một đơn có thể có nhiều đánh giá. Bài 8 lấy trung bình theo Order_ID trước khi left join với items; đơn không có đánh giá giữ NULL. `avg` bỏ NULL, không điền 0. Điểm sản phẩm được tính trên các dòng hàng có điểm đơn, không phải đánh giá trực tiếp riêng cho từng sản phẩm.

## 5. Chạy trên máy cá nhân

Notebook hiện hướng tới Colab: import `google.colab`, dùng đường dẫn `/content/`, và cell Java trên POSIX dò `/usr/lib/jvm`/cài qua `apt-get`. Chưa có lượt chạy local được kiểm chứng.

Nếu cần chạy local, dùng **bản sao** notebook, chuẩn bị PySpark 3.5.1 và JDK 17, chọn đúng kernel; bỏ qua cell upload chung và thay đường dẫn ở A.2 bằng `FE = "../data/fecom"` khi cwd là `Lab03/src/`. Trong cell tạo Spark, dùng Java đã cấu hình của máy thay đoạn tự dò/cài Java trên Colab. Chỉ chạy `prepare_data` khi đủ 5 CSV local để không gọi upload. Giữ nguyên các cell Bài 1–8 và kiểm tra đường dẫn trước khi đọc dữ liệu.

## 6. Xử lý lỗi thường gặp

| Hiện tượng | Kiểm tra và cách xử lý |
| --- | --- |
| `KeyError: 'data.zip'` | Cell upload đầu chỉ nhận đúng tên `data.zip`; tạo lại ZIP với thư mục `data/` bên trong và upload đúng file |
| Không thấy thư mục MovieLens dù chỉ chạy BTVN | Cell đầu vẫn liệt kê MovieLens; chuẩn bị ZIP gồm cả hai bộ như phần 2 |
| `FileNotFoundError`, `PATH_NOT_FOUND` hoặc A.2 báo thiếu CSV | Kiểm tra `/content/data/fecom`, tên file, file không rỗng và cấu trúc ZIP; bổ sung qua `prepare_data` |
| Chỉ đọc thành một cột hoặc thiếu cột | Dùng dấu `;`, có header; kiểm tra BOM/tên cột, không dùng dấu phẩy cho Fecom |
| Reviews lệch 99.223 dòng hoặc có điểm bất thường | Giữ `multiLine=True`, `escape='"'`; dùng đúng file gốc, không bỏ dòng để ép số lượng khớp |
| Assertion phiên bản Spark không đạt | Khởi động lại runtime và chạy cell cài 3.5.1 trước khi tạo Spark |
| Java gateway không khởi động | Kiểm tra traceback của cell Java, việc chọn/cài JDK 17 và `JAVA_HOME`; chạy lại từ runtime sạch khi cần |
| `NameError` với `orders`, `customer_lookup`, `items_money` | Chạy từ đầu theo thứ tự, đặc biệt hai cell Bài 1 và Bài 6 trước Bài 7 |
| Assertion số dòng/khóa/nối bảng thất bại | Đối chiếu đúng bộ dữ liệu; kiểm tra khóa trùng, NULL và cấu hình đọc CSV trước khi sửa thuật toán |
| Mất dữ liệu sau khi reset Colab | Upload lại ZIP và tạo lại các bảng; output lưu trong file không tạo biến cho runtime mới |

## 7. Kiểm tra và lưu kết quả

Đối chiếu đủ [Bài 1–8](result.md), gồm các bảng kiểm tra phép nối và đánh giá của Bài 8. Bản lưu có 13 cell code đều có output, không có output loại `error`; vẫn có log resolver ở cell pip như đã nêu.

Sau khi chạy trên bản sao, tải `.ipynb` có output về máy và mở lại để kiểm tra. Không dùng **Clear all outputs**. Không cần thêm Phần D vào notebook; dẫn [báo cáo PDF](../report/BaoCao.pdf). `data.zip` là file trung gian, không đưa vào Git.
