# Dữ liệu Lab01

Các số dòng bên dưới được đếm trực tiếp từ file trong repository; các file không có dòng tiêu đề.

## 1. Giao dịch: `trans/`

| File | Số dòng | Vai trò |
| --- | ---: | --- |
| [trans.txt](trans/trans.txt) | 60 | Dữ liệu giao dịch cho `TransAnalysis1`–`TransAnalysis6` |
| [cust.txt](trans/cust.txt) | 10 | Tra tên và tuổi khách hàng qua Distributed Cache ở B.5–B.6 |

Cấu trúc giao dịch, phân cách bằng dấu phẩy:

```text
TransID,Date,CustID,Cost,Game,Equipment,City,State,Mode
00000000,06-26-2011,4000001,040.33,Exercise & Fitness,Cardio Machine Accessories,Clarksville,Tennessee,credit
```

Ví dụ ngày trong file hiện tại là `06-26-2011`. Tên môn thể thao có ký tự `&`, tên thiết bị có khoảng trắng; không tách bản ghi bằng khoảng trắng.

Cấu trúc khách hàng:

```text
CustID,FirstName,LastName,Age,Profession
4000001,Kristina,Chung,55,Pilot
```

Các dòng đầu trong hai code block là mô tả schema, không phải header có sẵn trong file.

## 2. Đánh giá phim: `movielens/`

| File | Số dòng | Vai trò |
| --- | ---: | --- |
| [movies.txt](movielens/movies.txt) | 50 | Tên và thể loại phim |
| [ratings_1.txt](movielens/ratings_1.txt) | 50 | Phần thứ nhất của dữ liệu đánh giá |
| [ratings_2.txt](movielens/ratings_2.txt) | 50 | Phần thứ hai của dữ liệu đánh giá |
| [users.txt](movielens/users.txt) | 50 | Thông tin người dùng, gồm giới tính |

```text
movies.txt  : MovieID, Title, Genres
ratings_1/2 : UserID, MovieID, Rating, Timestamp
users.txt   : UserID, Gender, Age, Occupation, Zip-code
```

Các thể loại trong `Genres` được ngăn bằng `|`. Ví dụ:

```text
1043, Toy Story (1995), Animation|Children|Comedy
537, 1043, 4.0, 964982703
537, F, 25, 10, 48067
```

Dữ liệu có khoảng trắng sau dấu phẩy; mã Java phần đánh giá phim dùng `trim()` khi lấy các trường. `GenreRatingAverage` tra thể loại từ `movies.txt`; `GenderRatingAverage` dùng reduce-side join cho phim và đánh giá, đồng thời tra giới tính từ `users.txt` qua Distributed Cache.

## 3. Phân biệt với dữ liệu Lab02

[Lab02/data/movielens-mini/](../../Lab02/data/movielens-mini/) là bộ dữ liệu khác: có 184 dòng đánh giá (84 + 100) và thêm `occupation.txt`; Lab01 có 100 dòng đánh giá. Hai file giao dịch `trans240_1.txt`, `trans240_2.txt` nằm ở [Lab02/data/trans/](../../Lab02/data/trans/), không phải đầu vào của Lab01 hiện tại.

Không đối chiếu trực tiếp kết quả số giữa hai bộ dữ liệu này. Notebook Lab02 hiện chỉ giải các bài OpenFlights.

## 4. Đưa dữ liệu lên HDFS

Chạy từ thư mục `Lab01/data/` trong Cloudera VM đã cấu hình Hadoop:

```bash
hdfs dfs -mkdir -p /user/cloudera/lab1/trans
hdfs dfs -mkdir -p /user/cloudera/lab1/ml
hdfs dfs -mkdir -p /mycache
hdfs dfs -put -f trans/trans.txt /user/cloudera/lab1/trans/
hdfs dfs -put -f trans/cust.txt /mycache/cust
hdfs dfs -put -f movielens/movies.txt movielens/ratings_1.txt movielens/ratings_2.txt movielens/users.txt /user/cloudera/lab1/ml/
hdfs dfs -ls -R /user/cloudera/lab1
hdfs dfs -ls /mycache
```

`TransAnalysis5` và `TransAnalysis6` dùng URI `hdfs://localhost:8020/mycache/cust`, nên file cache phải mang tên `cust` không có đuôi `.txt`. Các bài đánh giá phim dùng file tra cứu dưới `/user/cloudera/lab1/ml/` theo URI ghi trong mã nguồn.

Xem [hướng dẫn Lab01](../docs/Huong_dan_Lab1_Hadoop_MapReduce.md) để biên dịch, export JAR và chạy từng bài. Hướng dẫn mô tả việc gom dữ liệu vào một thư mục trong VM; cấu trúc dữ liệu trong GitHub được trình bày ở trên.

Repository chưa có nguồn tải và điều kiện sử dụng được xác minh cho các file giao dịch, đánh giá phim của Lab01; cần bổ sung nếu xác định được nguồn tài liệu môn học.
