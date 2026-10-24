# Hướng dẫn Lab02 – Bài tập về nhà OpenFlights

Tài liệu dành cho phần **bài tập về nhà**, sử dụng [notebook OpenFlights](../src/Lab02_BTVN.ipynb). Hướng dẫn ưu tiên Google Colab, nơi notebook đã lưu output; phần local là cách chuẩn bị dựa trên đường dẫn và mã thiết lập hiện có, chưa phải một lần chạy local đã được ghi nhận.

## Mục lục

- [1. Chuẩn bị](#1-chuẩn-bị)
- [2. Chạy trên Google Colab](#2-chạy-trên-google-colab)
- [3. Chạy trên máy cá nhân](#3-chạy-trên-máy-cá-nhân)
- [4. Xử lý lỗi thường gặp](#4-xử-lý-lỗi-thường-gặp)
- [5. Kiểm tra và lưu kết quả](#5-kiểm-tra-và-lưu-kết-quả)

## 1. Chuẩn bị

- Trình duyệt và tài khoản Google để dùng Colab.
- Tải [src/Lab02_BTVN.ipynb](../src/Lab02_BTVN.ipynb) về máy, giữ đuôi `.ipynb`.
- Tải đủ 5 file từ [data/openflights/](../data/openflights/): `routes.dat`, `airports.dat`, `airlines.dat`, `planes.dat`, `countries.dat`. Dùng file gốc trong repository khi đối chiếu kết quả.
- Runtime Python có PySpark và Java tương thích. Notebook dùng `local[*]`, không có cấu hình yêu cầu GPU hoặc cụm Hadoop riêng.

### Phiên bản có thể xác minh

| Thành phần | Căn cứ |
| --- | --- |
| PySpark | Cell thiết lập cài `pyspark==3.5.1` **chỉ khi** import PySpark thất bại. Nếu runtime có sẵn phiên bản khác, cell sẽ dùng phiên bản đó. |
| Python | Metadata notebook khai báo `3.10`; chưa có output `sys.version` xác nhận runtime gốc. |
| Java | Notebook không cài hoặc in phiên bản Java; chưa xác minh được phiên bản runtime gốc. |
| Spark | `SparkSession.builder.appName('Lab2_OpenFlights').master('local[*]').getOrCreate()`. |

Theo [tài liệu Spark 3.5.1](https://archive.apache.org/dist/spark/docs/3.5.1/), Spark hỗ trợ Java 8/11/17 và yêu cầu Python từ 3.8; Java 8 trước 8u371 đã bị deprecated. Để chuẩn bị local, có thể chọn **Python 3.10 và JDK 17** làm cấu hình tương thích với căn cứ trên; đây là lựa chọn để chạy lại, không phải thông số đã xác nhận của Colab gốc. Không suy ra mọi phiên bản Python mới hơn đều đã được kiểm chứng.

## 2. Chạy trên Google Colab

### Bước 1. Mở Colab

Truy cập [Google Colab](https://colab.research.google.com/) và đăng nhập tài khoản Google. Kết nối một runtime Python.

### Bước 2. Mở notebook

Chọn **File → Upload notebook** (hoặc thẻ **Upload** trong hộp mở notebook), chọn `Lab02_BTVN.ipynb` đã tải từ repository. Tên mục có thể khác theo ngôn ngữ giao diện.

### Bước 3. Chuẩn bị PySpark

Cell thiết lập Spark trong notebook có sẵn cơ chế cài đặt khi thiếu thư viện:

```python
try:
    from pyspark.sql import SparkSession
except ImportError:
    import sys, subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'pyspark==3.5.1'])
    from pyspark.sql import SparkSession
```

Để chủ động dùng đúng phiên bản cài đặt được ghi trong notebook, chạy đoạn dưới trong một cell chuẩn bị của **bản sao trên Colab**, trước khi khởi tạo Spark:

```python
import sys, subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'pyspark==3.5.1'])
```

Nếu PySpark đã được import hoặc Spark đã khởi tạo trước khi đổi phiên bản, khởi động lại runtime rồi tiếp tục. Không coi cài đặt thành công là bằng chứng phiên bản đang được nạp; kiểm tra:

```python
import sys
import pyspark

print("Python:", sys.version)
print("PySpark:", pyspark.__version__)
subprocess.run(["java", "-version"], check=True)
```

Cần thấy PySpark `3.5.1` và Java thuộc nhóm tương thích nêu ở phần chuẩn bị. Nếu runtime Colab hiện tại có Python/Java không tương thích, chọn runtime tương thích nếu giao diện cho phép, hoặc dùng cấu hình local ở phần 3; notebook không chứa quy trình thay Java/Python trên Colab.

### Bước 4. Upload 5 file dữ liệu

Chạy cell code đầu tiên, chọn đồng thời đủ 5 file `.dat`. Đây là đoạn upload có sẵn trong notebook:

```python
from google.colab import files
import os
import shutil

# Thu muc luu du lieu
data_dir = "/content/data/openflights"
os.makedirs(data_dir, exist_ok=True)

# Upload 5 file .dat
uploaded = files.upload()

for filename in uploaded:
    shutil.move(
        f"/content/{filename}",
        f"{data_dir}/{filename}"
    )

# Kiem tra du 5 file
required_files = [
    "routes.dat",
    "airports.dat",
    "airlines.dat",
    "planes.dat",
    "countries.dat"
]

for filename in required_files:
    path = os.path.join(data_dir, filename)
    if os.path.exists(path):
        print(f"OK: {filename}")
    else:
        print(f"THIEU: {filename}")
```

### Bước 5. Kiểm tra đường dẫn

Cell upload chuyển file từ `/content/` vào:

```text
/content/data/openflights/
├── routes.dat
├── airports.dat
├── airlines.dat
├── planes.dat
└── countries.dat
```

Output phải có đủ 5 dòng `OK:`. Giữ nguyên tên file; tên như `routes (1).dat` không đáp ứng kiểm tra `routes.dat`. Colab mặc định làm việc ở `/content`; cell upload dùng đường dẫn tuyệt đối này, nên không đổi thư mục làm việc trước khi upload. Nếu cần, chạy `%cd /content` trong một cell Colab rồi upload lại.

### Bước 6. Khởi tạo SparkSession và SparkContext

Chạy cell code thứ hai sau khi dữ liệu đã sẵn sàng. Ngoài phần import/cài PySpark, cell có:

```python
import csv
from pathlib import Path
from operator import add

spark = SparkSession.builder.appName('Lab2_OpenFlights').master('local[*]').getOrCreate()
sc = spark.sparkContext
sc.setLogLevel('ERROR')

thu_muc = [Path('data/openflights'), Path('../data/openflights'),
            Path('/content/data/openflights')]
OF = next((p.resolve() for p in thu_muc if (p / 'routes.dat').exists()), None)
if OF is None:
    raise FileNotFoundError('Khong tim thay thu muc data/openflights')
print('Duong dan:', OF)
```

Trên Colab, output đã lưu là `Duong dan: /content/data/openflights`. Bộ dò đường dẫn chỉ kiểm tra `routes.dat`, vì vậy vẫn cần kiểm tra đủ cả 5 file ở bước trước.

### Bước 7. Chạy toàn bộ notebook

Chọn **Runtime → Run all**. Cell upload sẽ chạy lại và chờ thao tác; chọn lại cùng 5 file gốc để lượt chạy tiếp tục. Sau khi cell upload chuyển các file, các cell còn lại chạy theo thứ tự từ thiết lập Spark đến Bài 7.

Có thể thực hiện một lượt từ đầu bằng **Run all**, upload khi được hỏi, rồi chờ các bài chạy xong. Nếu chỉ chạy tiếp sau bước 6, chạy lần lượt toàn bộ cell Bài 1–7. Không bỏ qua Bài 1 vì các bài sau dùng RDD và bảng broadcast tạo ở đó; Bài 3 còn dùng `luot_di` của Bài 2.

### Bước 8. Đối chiếu output

Kiểm tra đầy đủ các cell Bài 1–7, kể cả cell thống kê hãng bay thứ hai của Bài 6. Đối chiếu bảng và các phép kiểm tra tổng trong [result.md](result.md). Nếu có lỗi, xử lý trước khi lưu notebook kết quả.

### Bước 9. Tải notebook có output

Chọn **File → Download → Download .ipynb** sau khi chạy xong. Không chọn xóa output; mở lại file đã tải để kiểm tra kết quả vẫn còn. Có thể lưu với tên khác trên máy để giữ bản gốc trong repository.

## 3. Chạy trên máy cá nhân

### Môi trường

Chuẩn bị Python 3.10, JDK 17 và môi trường notebook như VS Code với hỗ trợ Jupyter hoặc JupyterLab. Đây là cấu hình đề xuất dựa trên metadata và tài liệu tương thích, chưa được chạy lại trong quá trình soạn tài liệu.

Trong terminal của môi trường Python sẽ dùng làm kernel:

```bash
python --version
java -version
python -m pip install "pyspark==3.5.1"
python -m pip show pyspark
```

Java phải nằm trong `PATH` hoặc được trỏ tới qua `JAVA_HOME`, theo [hướng dẫn Spark 3.5.1](https://archive.apache.org/dist/spark/docs/3.5.1/). Chọn kernel dùng đúng môi trường vừa cài PySpark: **Select Kernel → Python Environments** trong VS Code, hoặc chọn kernel tương ứng trong Jupyter.

### Đặt dữ liệu và xử lý cell Colab

1. Giữ cấu trúc `Lab02/src/Lab02_BTVN.ipynb` và `Lab02/data/openflights/*.dat`.
2. Mở một bản sao notebook. **Bỏ qua cell upload đầu tiên** có `from google.colab import files`; API này dành cho Colab. Khi dùng Run all trên local, loại bỏ hoặc vô hiệu hóa cell đó trong bản sao.
3. Đặt thư mục làm việc của kernel là `Lab02/` hoặc `Lab02/src/`. Khi đó cell thiết lập tự tìm lần lượt `data/openflights` hoặc `../data/openflights`.
4. Nếu kernel đang ở gốc repository, sửa danh sách đường dẫn trong bản sao thành:

```python
thu_muc = [Path('Lab02/data/openflights')]
```

5. Chạy cell thiết lập Spark, kiểm tra `OF` trỏ đúng dữ liệu rồi chạy Bài 1–7 theo thứ tự.

Có thể kiểm tra trước đường dẫn bằng:

```python
from pathlib import Path
print("Thu muc lam viec:", Path.cwd())
```

Các thay đổi trên chỉ phục vụ bản sao chạy local; không cần đổi dữ liệu hoặc thuật toán RDD. Notebook không có cấu hình cụm từ xa hay cấu hình riêng cho từng máy Windows.

## 4. Xử lý lỗi thường gặp

Output được lưu trong notebook không có cell lỗi; báo cáo cũng không ghi nhận các lỗi dưới đây đã xảy ra. Đây là các trường hợp tham khảo từ mã thiết lập và điều kiện môi trường.

| Hiện tượng | Kiểm tra và cách xử lý |
| --- | --- |
| `ModuleNotFoundError: No module named 'pyspark'` | Chạy cell thiết lập hoặc lệnh cài `pyspark==3.5.1` bằng đúng Python của kernel. Khởi động lại kernel nếu vừa đổi phiên bản đã import. |
| `FileNotFoundError`, `PATH_NOT_FOUND` hoặc thiếu dữ liệu | Kiểm tra `Path.cwd()`, `OF`, đủ 5 tên file và các thư mục tìm kiếm ở bước 6. Trên Colab, upload lại vào `/content/data/openflights`. |
| `NameError: name 'sc' is not defined` hoặc SparkContext đã dừng | Chạy lại cell thiết lập Spark. Sau khi reset runtime, chạy lại Bài 1 để tạo RDD/broadcast và chạy các bài tiếp theo theo thứ tự. |
| Colab reset, mất file đã upload | File trong `/content` là dữ liệu của phiên runtime; upload lại 5 file và chạy lại toàn bộ notebook. Notebook có output không có nghĩa runtime mới đã có dữ liệu hoặc biến. |
| Không import được `google.colab` trên local | Bỏ qua hoặc vô hiệu hóa cell upload trong bản sao local, dùng dữ liệu đã có trong `Lab02/data/openflights/`. |
| Lỗi Java/PySpark, Java gateway không khởi động | Kiểm tra `java -version`, `pyspark.__version__`, `sys.version`; dùng Java tương thích, đúng kernel và `JAVA_HOME` nếu cần. Đổi phiên bản xong thì khởi động lại kernel. Không tự thêm cấu hình không có căn cứ chỉ từ tên lỗi gateway. |
| Lượt Run all chờ ở cell upload | Chọn lại đủ 5 file gốc trong hộp upload; đây là thao tác tương tác của notebook. |

## 5. Kiểm tra và lưu kết quả

- So sánh với [kết quả Bài 1–7](result.md), dùng cùng bộ dữ liệu và cùng điều kiện lọc mã IATA.
- Các tổng kiểm tra cần khớp 67.663 bản ghi. Bài 7 có tổng 3 nhóm; tỉ lệ quốc tế chỉ tính trên nhóm phân loại được.
- Bài 6 in nhãn quốc tế là 162 theo phép lấy phần bù của nhóm nội địa; đọc kèm giải thích 161 quốc tế xác định được và 1 SGN → THD chưa phân loại.
- Bài giải chỉ dùng RDD; giữ cách xử lý này khi chạy lại. Việc import `SparkSession` không có nghĩa các bài sử dụng DataFrame hoặc Spark SQL.
- Lưu `.ipynb` có output: trên Colab dùng bước 9, trên VS Code/Jupyter lưu notebook sau khi chạy hết. Mở lại bản lưu để kiểm tra đủ output, không dùng thao tác Clear all outputs.
