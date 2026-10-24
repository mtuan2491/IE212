# Lab02 – Apache Spark RDD

Lab02 gồm **thực hành trên lớp** về RDD, TransAnalysis và MovieLens, cùng **bài tập về nhà** phân tích mạng bay OpenFlights. Hai notebook độc lập, đều có output đã lưu từ Google Colab và dùng Spark trên một máy với `master('local[*]')`.

| Nội dung | Notebook | Dữ liệu | Hướng dẫn và kết quả |
| --- | --- | --- | --- |
| Thực hành trên lớp | [Lab02_ThucHanh.ipynb](src/Lab02_ThucHanh.ipynb) | [movielens-mini/](data/movielens-mini/), [trans/](data/trans/) | [Hướng dẫn thực hành](docs/Huong_dan_Lab2_Thuc_Hanh.md), gồm kết quả đối chiếu |
| Bài tập về nhà | [Lab02_BTVN.ipynb](src/Lab02_BTVN.ipynb) | [openflights/](data/openflights/) | [Hướng dẫn BTVN](docs/Huong_dan_Lab2_BTVN.md), [kết quả Bài 1–7](docs/result.md), [báo cáo PDF](report/BaoCao.pdf) |

## Thực hành trên lớp

Notebook gồm Phần A chuẩn bị PySpark 3.5.1 và dữ liệu; Phần B tạo RDD, partition, lazy evaluation và caching; Phần C giải TransAnalysis1–6 bằng RDD và broadcast; Phần D phân tích MovieLens theo phim, thể loại, giới tính, nhóm tuổi và nghề nghiệp.

Output ghi nhận 184 lượt đánh giá, 50 phim, 50 người dùng và 240 giao dịch. Phần D có 14 phim được đánh giá; 471 lượt theo thể loại do mỗi phim có thể thuộc nhiều thể loại. Kết quả và cách chạy lại được trình bày trong [hướng dẫn thực hành](docs/Huong_dan_Lab2_Thuc_Hanh.md).

## Bài tập về nhà – OpenFlights

Phần BTVN dùng RDD để đọc, biến đổi, tổng hợp và phân loại dữ liệu OpenFlights. Các bảng kỹ thuật, dữ liệu và Bài 1–7 bên dưới thuộc notebook BTVN.

## Nội dung và kỹ thuật BTVN

| Nhóm | API được dùng trong notebook |
| --- | --- |
| Đọc và tái sử dụng dữ liệu | `sc.textFile()`, `cache()` |
| Transformations | `map()`, `flatMap()`, `filter()`, `reduceByKey()`, `distinct()`, `values()` |
| Actions | `count()`, `first()`, `takeOrdered()`, `sum()`, `max()`, `collect()`, `collectAsMap()` |
| Bảng tra | `collectAsMap()` tạo dictionary; `sc.broadcast()` chia sẻ bảng tra sân bay và hãng bay |
| Tách dữ liệu | `split(',')` cho đường bay, `csv.reader()` cho sân bay và hãng bay có trường chứa dấu phẩy |

Các bài giải dùng RDD, không dùng DataFrame, Spark SQL hay pandas. `SparkSession` được tạo để lấy `spark.sparkContext`.

## Bộ dữ liệu BTVN

Năm file nằm trong [data/openflights/](data/openflights/), định dạng văn bản phân cách bằng dấu phẩy, không có header. Số dòng được đếm trực tiếp trên bản dữ liệu đi kèm:

| File | Số dòng | Số cột | Vai trò trong BTVN |
| --- | ---: | ---: | --- |
| [routes.dat](data/openflights/routes.dat) | 67.663 | 9 | Bản ghi đường bay: hãng, sân bay đi/đến, codeshare, điểm dừng, loại máy bay; dùng trong Bài 1–7 |
| [airports.dat](data/openflights/airports.dat) | 7.698 | 14 | Thông tin sân bay; tra tên, thành phố, quốc gia qua mã IATA hợp lệ |
| [airlines.dat](data/openflights/airlines.dat) | 6.162 | 8 | Thông tin hãng; Bài 6 tra bằng Airline ID để lấy tên và mã IATA |
| [planes.dat](data/openflights/planes.dat) | 246 | 3 | Tên máy bay, mã IATA/ICAO; được upload nhưng chưa được notebook đọc |
| [countries.dat](data/openflights/countries.dat) | 261 | 3 | Tên quốc gia/vùng lãnh thổ, mã ISO và DAFIF; được upload nhưng chưa được notebook đọc |

Bài 4 đếm trực tiếp mã Equipment trong `routes.dat`; Bài 5–7 lấy quốc gia từ `airports.dat`. Hai thư mục `data/trans/` và `data/movielens-mini/` dành cho notebook thực hành trên lớp; notebook BTVN không sử dụng chúng.

Trong tài liệu này, **số đường bay** là số bản ghi trong `routes.dat` theo phép đếm của notebook, không phải tần suất chuyến bay thực tế hay số cặp sân bay duy nhất. Bảng tra sân bay chỉ giữ mã có đúng 3 ký tự chữ theo điều kiện `len(p[4]) == 3 and p[4].isalpha()`.

### Nguồn và điều kiện sử dụng

Nguồn: [OpenFlights](https://openflights.org/data.php), [repository dữ liệu gốc](https://github.com/jpatokal/openflights/tree/master/data). Địa chỉ `https://openflights.org/data.html` được nêu trong yêu cầu hiện trả lỗi khi kiểm tra; liên kết `.php` ở trên truy cập được. OpenFlights ghi nhận dữ liệu đường bay ngừng được cập nhật từ tháng 6/2014; các kết quả chỉ mô tả bản dữ liệu đang lưu trong repository. Chưa xác minh được thời điểm tải và commit nguồn của từng file.

Trang nguồn công bố các cơ sở dữ liệu Airport, Airline, Plane và Route theo [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/), nội dung riêng lẻ theo [Database Contents License (DbCL)](https://opendatacommons.org/licenses/dbcl/1-0/). Khi tái sử dụng hoặc phân phối, cần giữ ghi nhận nguồn và tuân thủ điều kiện tương ứng; xem phần Licensing and disclaimer trên trang OpenFlights. Trang này không nêu riêng điều kiện cho `countries.dat`, nên không gán thêm giấy phép cho file đó khi chưa xác minh.

## Các bài tập về nhà

| Bài | Mục tiêu | Kết quả chính |
| --- | --- | --- |
| 1. Đọc dữ liệu và kiểm tra | Đếm dòng/cột, kiểm tra IATA, tạo bảng tra | 67.663 đường bay; 7.698 sân bay; 6.162 hãng; 6.071 mã IATA hợp lệ |
| 2. Sân bay bận rộn nhất | Đếm đường bay đi/đến, xếp hạng theo số đường bay đi | ATL dẫn đầu với 915 đường bay đi |
| 3. Số hãng bay khai thác mỗi sân bay | Loại trùng cặp sân bay đi–mã hãng và đếm | 19.288 cặp; CDG dẫn đầu với 108 hãng |
| 4. Thống kê theo loại máy bay | Tách từng mã Equipment bằng `flatMap()` | 168 mã loại máy bay; 93.231 cặp đường bay–loại máy bay |
| 5. Số đường bay theo quốc gia | Tra quốc gia sân bay đi, tổng hợp theo quốc gia | 225 giá trị quốc gia/vùng lãnh thổ; 406 bản ghi không tra được sân bay đi |
| 6. Mạng bay Việt Nam | Lọc đường bay đi/đến Việt Nam, thống kê sân bay và hãng | 288 đường bay đi; 126 nội địa; 162 còn lại gồm 161 quốc tế xác định được và 1 chưa phân loại |
| 7. Nội địa so với quốc tế trên toàn thế giới | Phân loại theo quốc gia của hai đầu đường bay | 32.167 nội địa; 34.767 quốc tế; 729 không tra được |

Theo báo cáo, Bài 1–6 thuộc phần bắt buộc và Bài 7 thuộc phần tự chọn; cả 7 bài đều có trong notebook.

## Cấu trúc thư mục

```text
Lab02/
├── README.md
├── src/
│   ├── Lab02_ThucHanh.ipynb
│   └── Lab02_BTVN.ipynb
├── data/
│   ├── openflights/
│   │   ├── routes.dat
│   │   ├── airports.dat
│   │   ├── airlines.dat
│   │   ├── planes.dat
│   │   └── countries.dat
│   ├── trans/
│   │   ├── trans240_1.txt
│   │   ├── trans240_2.txt
│   │   └── cust.txt
│   └── movielens-mini/
│       ├── movies.txt
│       ├── ratings_1.txt
│       ├── ratings_2.txt
│       ├── users.txt
│       └── occupation.txt
├── docs/
│   ├── Huong_dan_Lab2_Thuc_Hanh.md
│   ├── Huong_dan_Lab2_BTVN.md
│   └── result.md
└── report/
    └── BaoCao.pdf
```

## Chạy nhanh

- **Thực hành trên lớp:** tải [Lab02_ThucHanh.ipynb](src/Lab02_ThucHanh.ipynb), chuẩn bị `data.zip` chứa `data/movielens-mini/` và `data/trans/`, rồi chạy Phần A → D theo [hướng dẫn](docs/Huong_dan_Lab2_Thuc_Hanh.md).
- **BTVN:** dùng [Lab02_BTVN.ipynb](src/Lab02_BTVN.ipynb) với 5 file OpenFlights `.dat` theo [hướng dẫn BTVN](docs/Huong_dan_Lab2_BTVN.md).

### Chạy BTVN trên Colab

Mở [Google Colab](https://colab.research.google.com/), tải [notebook](src/Lab02_BTVN.ipynb) lên và upload đủ 5 file `.dat` bằng cell đầu tiên. Cell tiếp theo thiết lập Spark và tìm dữ liệu tại `/content/data/openflights`. Sau khi chuẩn bị xong, chạy các cell theo thứ tự.

Xem [hướng dẫn chạy](docs/Huong_dan_Lab2_BTVN.md) để cài đúng PySpark, xử lý cell upload khi chạy lại toàn bộ notebook và chuẩn bị môi trường local.

## Kết quả và báo cáo BTVN

[Kết quả Bài 1–7](docs/result.md) trình bày các bảng xếp hạng, số liệu kiểm tra và lưu ý cách đếm. Đặc biệt, output Bài 6 ghi nhãn `Chuyen bay quoc te di: 162`, nhưng có 1 bản ghi SGN → THD chưa tra được quốc gia đến; chỉ 161 bản ghi được xác định là quốc tế.

Báo cáo đầy đủ: [report/BaoCao.pdf](report/BaoCao.pdf).
