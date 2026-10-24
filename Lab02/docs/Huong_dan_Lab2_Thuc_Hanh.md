# Hướng dẫn Lab02 – Thực hành trên lớp với Spark RDD

Tài liệu môn **IE212 – Công nghệ dữ liệu lớn**, chủ đề **Lab 2 – Apache Spark RDD**, dành cho [Lab02_ThucHanh.ipynb](../src/Lab02_ThucHanh.ipynb). Mục tiêu là tìm hiểu RDD, transformations, actions, lazy evaluation, caching, xử lý giao dịch và phân tích MovieLens bằng PySpark trên Google Colab.

Đây là phần **thực hành trên lớp**. Phần bài tập về nhà OpenFlights có [notebook](../src/Lab02_BTVN.ipynb), [hướng dẫn](Huong_dan_Lab2_BTVN.md) và [kết quả](result.md) riêng.

## Mục lục

- [1. Nội dung notebook](#1-nội-dung-notebook)
- [2. Cấu trúc dữ liệu](#2-cấu-trúc-dữ-liệu)
- [3. Chạy trên Google Colab](#3-chạy-trên-google-colab)
- [4. Chạy trên VS Code local](#4-chạy-trên-vs-code-local)
- [5. Kết quả mong đợi](#5-kết-quả-mong-đợi)
- [6. Lỗi thường gặp](#6-lỗi-thường-gặp)
- [7. Lưu kết quả](#7-lưu-kết-quả)

## 1. Nội dung notebook

Notebook đã điền các vị trí TODO và có output cho cả 32 cell code. Các chú thích TODO còn lại là phần mô tả bài tập, không có nghĩa code vẫn để trống. Chạy theo thứ tự Phần A → B → C → D.

### Phần A – Chuẩn bị môi trường

Cài `pyspark==3.5.1`, upload và giải nén `data.zip` nếu thiếu dữ liệu trên Colab; tạo `SparkSession` với tên `IE212-Lab2`, `master("local[*]")`, rồi lấy `sc = spark.sparkContext`. Cell A.2 đặt các biến `DATA`, `ML`, `TR` và liệt kê file để kiểm tra đường dẫn trước khi đọc RDD.

### Phần B – Làm quen với Spark RDD

Dùng `sc.parallelize()` tạo RDD chia 2 partition; so sánh `map()` với action `collect()` để quan sát lazy evaluation. Đọc hai file ratings bằng `textFile()` và `union()`, tách trường, ép kiểu và tạo các RDD MovieLens dùng tiếp ở Phần D. So sánh thời gian `count()` khi có và không có `cache()`; kết quả thời gian phụ thuộc runtime, không phải ngưỡng bắt buộc.

### Phần C – TransAnalysis bằng RDD

Giải lại sáu dạng bài TransAnalysis của Lab01:

| Bài | Mục tiêu và kỹ thuật chính |
| --- | --- |
| TransAnalysis1 | Tổng tiền theo loại hình: `map()`, `reduceByKey()` |
| TransAnalysis2 | Gom mã khách theo giao dịch và tổng tiền: tuple, `groupByKey()`, `mapValues()`; mã khách có thể lặp |
| TransAnalysis3 | Danh sách khách phân biệt: `distinct()` trên cặp (loại hình, CustID), rồi `groupByKey()` |
| TransAnalysis4 | Đếm khách phân biệt mỗi loại hình từ RDD cặp đã khử trùng: `mapValues()`, `reduceByKey()` |
| TransAnalysis5 | Thay mã bằng tên khách bằng bảng nhỏ từ `collectAsMap()` và `sc.broadcast()` |
| TransAnalysis6 | Tra tên kèm tuổi, gom theo loại hình và sắp xếp danh sách |

RDD cho phép nối các phép biến đổi và dùng lại kết quả trung gian; `reduceByKey()` thay phần cộng gộp của Mapper/Reducer, broadcast phục vụ tra cứu bảng nhỏ tương tự Distributed Cache của Hadoop. Khi so sánh, cần phân biệt tổng theo mọi giao dịch với số khách đã khử trùng.

**Lưu ý bộ dữ liệu:** notebook mô tả đây là bộ giao dịch của Lab01, nhưng file thực tế trong repository hiện khác nhau: `Lab01/data/trans/trans.txt` có 60 dòng, còn hai file `trans240_*.txt` của Lab02 có tổng 240 dòng. Vì vậy chỉ so sánh cách xử lý; không yêu cầu các tổng của hai Lab trùng nhau khi dùng các file hiện có.

### Phần D – Phân tích MovieLens

| Mục | Mục tiêu và kỹ thuật chính |
| --- | --- |
| D.1 – Theo phim | Tính tổng điểm và số lượt bằng `reduceByKey()`, chia để lấy trung bình, `join()` lấy tên phim; tìm phim cao điểm nhất có ít nhất 5 lượt. Đối chiếu với cách dùng `groupByKey()` |
| D.2 – Theo thể loại | `flatMap()` tách chuỗi Genres theo ký tự `\|`, `join()` với ratings rồi cộng tổng và đếm theo thể loại |
| D.3 – Theo giới tính | Nối theo UserID, đổi khóa sang MovieID, tính riêng nam/nữ; kiểm tra cách dựng dữ liệu bằng `join()` và broadcast cho cùng kết quả |
| D.4 – Theo nhóm tuổi | Phân nhóm, nối theo UserID rồi gộp theo khóa (MovieID, nhóm tuổi); hiển thị đủ 4 nhóm, ghi `N/A` nếu không có đánh giá |
| D.5 – Theo nghề nghiệp | Nối ratings với người dùng, gộp theo mã nghề, nối tên nghề; dùng `rightOuterJoin()` giữ cả nghề không có lượt đánh giá |

Trong notebook, Bài 4 và Bài 5 cùng nằm dưới tiêu đề **D.4. Bài 4 và Bài 5. Nhóm tuổi và nghề nghiệp**; bảng trên tách hai bài để tiện tra cứu. Hàm tuổi dùng các ngưỡng `<18`, `<35`, `<50`, còn lại là `50+`; nhãn `0-18` trong output thực tế tương ứng tuổi dưới 18, nhãn `18-35` tương ứng từ 18 đến dưới 35.

## 2. Cấu trúc dữ liệu

Các file là văn bản phân cách bằng dấu phẩy, không có header. Số dòng dưới đây được đếm từ dữ liệu trong repository; output notebook cũng xác nhận các tổng tương ứng.

| Thư mục | File | Số dòng | Vai trò/lược đồ |
| --- | --- | ---: | --- |
| [movielens-mini/](../data/movielens-mini/) | [movies.txt](../data/movielens-mini/movies.txt) | 50 | MovieID, Title, Genres; nhiều thể loại phân cách bằng ký tự `\|` |
| movielens-mini/ | [ratings_1.txt](../data/movielens-mini/ratings_1.txt) | 84 | UserID, MovieID, Rating, Timestamp |
| movielens-mini/ | [ratings_2.txt](../data/movielens-mini/ratings_2.txt) | 100 | Cùng lược đồ ratings_1; được nối bằng `union()` |
| movielens-mini/ | [users.txt](../data/movielens-mini/users.txt) | 50 | UserID, Gender, Age, Occupation, Zip-code; notebook không dùng Zip-code |
| movielens-mini/ | [occupation.txt](../data/movielens-mini/occupation.txt) | 15 | ID, Occupation; tra tên nghề từ mã nghề trong users |
| [trans/](../data/trans/) | [trans240_1.txt](../data/trans/trans240_1.txt) | 120 | Nửa đầu dữ liệu giao dịch |
| trans/ | [trans240_2.txt](../data/trans/trans240_2.txt) | 120 | Nửa sau, được nối với file đầu bằng `union()` |
| trans/ | [cust.txt](../data/trans/cust.txt) | 10 | CustID, FirstName, LastName, Age, Profession; tra tên và tuổi khách |

Lược đồ giao dịch: `TransID, Date, CustID, Cost, Game, Equipment, City, State, Mode`. Code dùng `p[2]` là mã khách, `p[3]` là số tiền, `p[4]` là loại hình thể thao.

Thư mục [openflights/](../data/openflights/) dành cho BTVN, không cần để chạy Phần B, C, D. Có thể để thư mục này trong ZIP đầy đủ; cell kiểm tra chỉ yêu cầu 8 file MovieLens và giao dịch nêu trên.

## 3. Chạy trên Google Colab

### Bước 1. Mở Colab

Mở [Google Colab](https://colab.research.google.com/), đăng nhập và kết nối runtime Python.

### Bước 2. Upload notebook

Tải [Lab02_ThucHanh.ipynb](../src/Lab02_ThucHanh.ipynb) về máy. Trong Colab, chọn **File → Upload notebook** hoặc thẻ **Upload** trong hộp mở notebook, rồi chọn file này. Dùng notebook đã có đầy đủ code, không cần tạo notebook mới.

### Bước 3. Chuẩn bị `data.zip`

ZIP phải chứa **thư mục `data/` ở cấp ngoài cùng**, rồi đến hai thư mục con. Khi giải nén vào `/content/`, cần có cấu trúc:

```text
/content/data/
├── movielens-mini/
│   ├── movies.txt
│   ├── ratings_1.txt
│   ├── ratings_2.txt
│   ├── users.txt
│   └── occupation.txt
└── trans/
    ├── trans240_1.txt
    ├── trans240_2.txt
    └── cust.txt
```

Cách nén toàn bộ dữ liệu trên Windows: mở PowerShell tại **`Lab02/`**, chạy:

```powershell
Compress-Archive -LiteralPath .\data -DestinationPath .\data.zip
```

Lệnh nén cả thư mục `data`, bao gồm OpenFlights nếu có. Nếu `data.zip` đã tồn tại, chọn nơi lưu mới hoặc chuyển bản ZIP cũ ra chỗ khác trước khi chạy. Mở ZIP để xác nhận thấy `data/movielens-mini/...` và `data/trans/...`.

Để tạo ZIP nhỏ chỉ chứa hai thư mục cần thiết, có thể chạy đoạn Python sau **trên máy cá nhân, với thư mục làm việc là gốc repository** (trong Python hoặc script tạm). File ZIP được tạo ở gốc, bên ngoài thư mục dữ liệu:

```python
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

with ZipFile("data.zip", "x", compression=ZIP_DEFLATED) as archive:
    for folder in ("movielens-mini", "trans"):
        for path in sorted((Path("Lab02/data") / folder).glob("*.txt")):
            archive.write(path, arcname=path.relative_to("Lab02").as_posix())
```

Chế độ `"x"` yêu cầu chưa có `data.zip` tại nơi tạo. Hai cách nén đều phải giữ tiền tố `data/`. ZIP chỉ chứa `movielens-mini/` và `trans/` ở gốc, hoặc chứa `Lab02/data/`, đều sai cấu trúc đối với cell giải nén hiện tại.

### Bước 4. Cài PySpark

Chạy cell cài đặt có sẵn ở Phần A:

```python
!pip install -q pyspark==3.5.1
```

Giữ phiên bản 3.5.1. Output cũ có thông báo resolver của pip về `dataproc-spark-connect 1.1.0` yêu cầu PySpark 4.0, trong khi notebook cài 3.5.1. Log này có tiền tố `ERROR:`, nhưng các cell tiếp theo trong bản lưu vẫn tạo Spark 3.5.1 và chạy đến cuối; không được coi log là bằng chứng mọi cell thất bại hoặc môi trường hoàn toàn không có cảnh báo. Xác nhận lại bằng cell tạo Spark ở bước 7.

### Bước 5. Upload dữ liệu bằng cell có sẵn

Chạy cell Phần A ngay dưới mục nạp dữ liệu. Code nhận diện Colab bằng `os.path.isdir("/content")`, kiểm tra 8 file và chỉ gọi `files.upload()` nếu còn thiếu. Khi hiện hộp chọn, upload đúng tên **`data.zip`**. Giữ thư mục làm việc Colab là `/content` để đường dẫn ZIP tương đối hoạt động đúng.

Không thêm cell upload khác. Nếu cả 8 file đã tồn tại, cell bỏ qua upload; điều này không tự xác minh dữ liệu cũ có cùng nội dung với repository, nên dùng runtime mới khi cần đối chiếu một lượt sạch với bộ dữ liệu gốc.

### Bước 6. Giải nén và kiểm tra cấu trúc

Cũng trong cell bước 5, notebook mở `zipfile.ZipFile("data.zip")`, gọi `extractall("/content/")`, rồi kiểm tra từng file dưới `/content/data`. Không cần chạy thêm lệnh giải nén.

Cell phải in `Da nap du 8 tep du lieu:`. Với ZIP nhỏ, danh sách có `movielens-mini` và `trans`; output đã lưu còn có `openflights` vì lần đó upload ZIP đầy đủ. Thư mục bổ sung này không ảnh hưởng phần thực hành. Nếu xuất hiện `FileNotFoundError` về cấu trúc ZIP, sửa ZIP trước khi chạy tiếp.

### Bước 7. Khởi tạo SparkSession và xác định đường dẫn

Chạy cell tạo `SparkSession` tiếp theo, kiểm tra output `3.5.1`. Cell này tạo cả `spark` và `sc`. Sau đó chạy cell A.2 xác định dữ liệu: `DATA = "/content/data"`, `ML` trỏ đến `movielens-mini`, `TR` trỏ đến `trans`. Output cần liệt kê đủ 5 file MovieLens và 3 file giao dịch.

### Bước 8. Chạy từ Phần A đến D theo thứ tự

Chạy tiếp Phần B để tạo RDD MovieLens, Phần C cho giao dịch, rồi Phần D để phân tích phim. Phần D phụ thuộc RDD tạo ở B; các bài C dùng lại `trans`, `cap`, `tong`, `bc_cust` của những cell trước.

Có thể dùng **Runtime → Run all** từ đầu; cell cài đặt sẽ chạy lại, cell dữ liệu có thể chờ upload nếu thiếu file. Cell code cuối gọi `spark.stop()`. Muốn tính tiếp sau đó, chạy lại cell khởi tạo Spark và các cell tạo RDD phụ thuộc, hoặc chạy lại toàn bộ notebook.

### Bước 9. Kiểm tra output

Đối chiếu các mốc ở phần [kết quả mong đợi](#5-kết-quả-mong-đợi), đặc biệt 184 đánh giá, 240 giao dịch, 44 cặp phân biệt và hai phép so sánh ra `True`. Không dùng thời gian đo cache hay thứ tự của `take()` làm tiêu chí khớp tuyệt đối.

### Bước 10. Tải notebook có output

Chọn **File → Download → Download .ipynb** sau khi chạy thành công. Giữ output và mở lại file tải xuống để kiểm tra; xem thêm [cách lưu trong repository](#7-lưu-kết-quả).

Colab mất dữ liệu trong `/content` khi runtime bị reset hoặc được tạo lại. Khi đó cần upload dữ liệu và chạy lại từ Phần A; output đang hiển thị không có nghĩa biến và file vẫn còn trong runtime mới.

## 4. Chạy trên VS Code local

Chuẩn bị Python 3.10, JDK 17 và PySpark 3.5.1. Đây là cấu hình để chạy lại dựa trên [tài liệu Spark 3.5.1](https://archive.apache.org/dist/spark/docs/3.5.1/) và phiên bản Spark được in trong notebook; chưa có lượt chạy local được xác minh ở lần cập nhật tài liệu này. Java cần nằm trong `PATH` hoặc được trỏ qua `JAVA_HOME`.

Trong terminal của môi trường Python sẽ dùng cho notebook:

```bash
python --version
java -version
python -m pip install "pyspark==3.5.1" ipykernel
python -m pip show pyspark
```

Trong VS Code có hỗ trợ Python/Jupyter, mở [notebook thực hành](../src/Lab02_ThucHanh.ipynb), chọn **Select Kernel → Python Environments**, rồi chọn môi trường vừa cài. Có thể bỏ qua cell `!pip install` nếu kernel đã có đúng PySpark.

Giữ `Lab02/src/Lab02_ThucHanh.ipynb` cạnh `Lab02/data/` theo cây thư mục repository. Cell upload chạy trước cell xác định đường dẫn để khai báo `os`, `TREN_COLAB`; trên máy không có `/content`, cell này tự bỏ qua upload. Không cần ZIP trên local.

Code thử lần lượt `Path.cwd() / "data"` rồi `Path.cwd().parent / "data"`, chọn thư mục chứa cả `movielens-mini/` và `trans/`. Vì vậy đặt thư mục làm việc của kernel là **`Lab02/` hoặc `Lab02/src/`**. Nếu chạy từ gốc repository thì hai đường dẫn dò hiện tại không tìm được `Lab02/data`; cần đổi thư mục làm việc trước khi chạy A.2. Có thể kiểm tra/đặt trong một cell tạm của bản sao local:

```python
from pathlib import Path
import os

print(Path.cwd())
# Chỉ chạy dòng dưới nếu cwd hiện là gốc repository:
os.chdir("Lab02")
```

Chạy các cell còn lại theo A → D và kiểm tra `ML`, `TR` trước khi đọc dữ liệu. Các gợi ý Windows trong notebook chưa được kiểm chứng bằng một lượt chạy local ở đây; nếu gặp lỗi Java/Hadoop, cần căn cứ traceback thực tế, không coi cài PySpark thành công là đủ xác nhận môi trường chạy được.

## 5. Kết quả mong đợi

Các số sau lấy trực tiếp từ **output đã lưu của notebook thực hành**; vị trí tra cứu dùng nhãn mục/cell trong notebook. Đây là mốc đối chiếu dữ liệu kèm repository, không phải kết quả của lượt chạy mới trong lần soạn hướng dẫn.

| Vị trí | Mốc đối chiếu đã xác nhận |
| --- | --- |
| A.1 – Tạo SparkSession | Spark `3.5.1` |
| B.1 – RDD đầu tiên | 2 partition; `collect()` ra `[1, 2, 3, 4, 5]` |
| B.1 – Lazy evaluation | Bình phương ra `[1, 4, 9, 16, 25]`; bản lưu đo sau map 0.0020 giây, sau collect 1.7217 giây |
| B.1 – Đọc MovieLens | 184 lượt đánh giá; 50 phim, 50 người dùng, 15 nghề |
| B.1 – Đo cache | Không cache: 0.325 và 0.260 giây; có cache: 0.328 và 0.201 giây, chỉ để tham khảo |
| C.1 – Đọc giao dịch | 240 giao dịch |
| C.1 – TransAnalysis1/2 | 13 loại hình; ví dụ Air Sports: 142.77, Outdoor Recreation: 6758.08, Winter Sports: 98.21 |
| C.1 – TransAnalysis3/4 | 44 cặp (loại hình, khách hàng) phân biệt; Air Sports có 1 khách, Water Sports có 7 khách |
| C.2 – Broadcast khách hàng | 10 khách; mã `4000001` tra được `('Kristina', '55')` |
| D.1 – Theo phim | 14 phim có đánh giá; Sunset Boulevard (1950) đạt 4.36 với 7 lượt, cao nhất khi yêu cầu ít nhất 5 lượt |
| D.1 – Hai cách gộp | So sánh kết quả `reduceByKey()` với `groupByKey()` ra `True` |
| D.2 – Theo thể loại | 50 phim sinh 122 cặp phim–thể loại; bảng đánh giá có 12 thể loại; tổng lượt theo thể loại là 471, còn ratings gốc là 184 |
| D.3 – Theo giới tính | So sánh dữ liệu dựng bằng `join()` và broadcast ra `True`; Psycho (1960) có `N/A, 4.00` theo thứ tự nam, nữ |
| D.4 – Theo tuổi | Phân bố người dùng: `18-35`: 23, `35-50`: 23, `50+`: 4; nhóm `0-18` không có người dùng, điểm nhóm này đều `N/A` |
| D.4 – Bài 5, nghề nghiệp | 14 nghề có đánh giá, tổng 184 lượt; bảng nghề có 15 nghề; outer join giữ 15 nghề và in `[('Researcher', 0)]` |
| Cell kết thúc | `Da dong SparkSession.` |

471 là **lượt đánh giá theo thể loại**: một đánh giá đóng góp cho mỗi thể loại của phim, nên không bằng 184 đánh giá gốc. Tương tự, 50 phim trong danh mục không có nghĩa cả 50 đều được đánh giá; chỉ 14 phim xuất hiện trong bảng phân tích.

Notebook không có output kiểu lỗi Python `error` ở các cell code, nhưng cell pip có log xung đột phụ thuộc như đã nêu. Thứ tự phần tử không được sắp xếp hoặc thứ tự phim cùng điểm có thể thay đổi; thời gian thực thi cũng thay đổi theo máy.

## 6. Lỗi thường gặp

| Hiện tượng | Cách kiểm tra và xử lý |
| --- | --- |
| Không tìm thấy dữ liệu | Trên Colab kiểm tra `/content/data/movielens-mini/` và `/content/data/trans/`; local kiểm tra cwd, `DATA`, `ML`, `TR` và đủ 8 file |
| `data.zip thieu file hoac sai cau truc` | Mở ZIP, kiểm tra có tiền tố `data/`; loại trường hợp lồng `Lab02/data/` hoặc thiếu thư mục ngoài `data/`, tạo lại ZIP rồi chạy cell nạp dữ liệu |
| `Can upload file data.zip` | Upload file đúng tên `data.zip` tại cwd `/content`; kiểm tra tránh tên tự thêm hậu tố khi upload trùng |
| `ModuleNotFoundError: pyspark` | Chạy cell cài 3.5.1 trên Colab hoặc cài bằng Python của kernel local; kiểm tra lại kernel được chọn |
| Chưa có `spark`/`sc` hoặc SparkContext đã dừng | Chạy lại cell tạo SparkSession và các cell tạo RDD; cell cuối notebook chủ động dừng Spark |
| Colab reset runtime | Kết nối lại, cài PySpark, upload ZIP và chạy từ A; cần tạo lại cả dữ liệu lẫn biến |
| `NameError` với `ratings`, `cap`, `bc_cust`, `r_theo_user` | Chạy các cell trước theo đúng thứ tự, vì phần sau dùng kết quả phần trước |
| Log pip có warning hoặc `ERROR: pip's dependency resolver...` | Đọc nội dung log; trong bản lưu đây là xung đột `dataproc-spark-connect` với PySpark 3.5.1. Kiểm tra Spark in `3.5.1` và các cell sau; không tự đổi sang 4.x để né thông báo |
| Traceback Python/Spark, cell dừng và không có output mong đợi | Đây là lỗi thực thi cần xử lý theo traceback, khác log resolver trong bản lưu. Kiểm tra Java, PySpark, dữ liệu và thứ tự cell trước khi chạy tiếp |

## 7. Lưu kết quả

Sau khi chạy xong A → D, tải file bằng **File → Download → Download .ipynb**. Không dùng **Clear all outputs**. Mở lại bản tải để kiểm tra đủ bảng TransAnalysis, MovieLens, hai dòng so sánh `True` và thông báo đóng Spark.

Nếu muốn cập nhật kết quả trong repository, lưu bản tải vào `Lab02/src/Lab02_ThucHanh.ipynb` sau khi đối chiếu với bản hiện có; giữ nguyên tên file để các liên kết tiếp tục hoạt động. Kiểm tra diff notebook trước khi commit để tránh mất code/output ngoài ý muốn. `data.zip` chỉ là file trung gian phục vụ upload, không cần thêm vào repository.

Hướng dẫn này chỉ yêu cầu lưu notebook có output; không bổ sung yêu cầu nộp PDF cho phần thực hành. [BaoCao.pdf](../report/BaoCao.pdf) được dẫn trong phần BTVN OpenFlights.
