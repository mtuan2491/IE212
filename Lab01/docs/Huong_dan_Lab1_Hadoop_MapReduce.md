# Lab 1 Hadoop & MapReduce – Hướng dẫn thực hiện tuần tự

Tài liệu này tổng hợp toàn bộ quy trình đã thực hiện cho Lab 1, từ chuẩn bị dữ liệu và mã nguồn trên Windows, đưa file vào Cloudera, nạp dữ liệu lên HDFS, tạo project trong Eclipse, export JAR, đến các lệnh chạy từng bài B.1–B.6 và C.1.1–C.1.3.

---

## 1. Chuẩn bị file trên Windows

Chuẩn bị các file dữ liệu mẫu:

```text
trans.txt
cust.txt
movies.txt
ratings_1.txt
ratings_2.txt
users.txt
```

Chuẩn bị 9 file Java:

```text
TransAnalysis1.java
TransAnalysis2.java
TransAnalysis3.java
TransAnalysis4.java
TransAnalysis5.java
TransAnalysis6.java
MovieRatingAverage.java
GenreRatingAverage.java
GenderRatingAverage.java
```

Nên gom thành:

```text
Lab01/
├── data/
│   ├── trans.txt
│   ├── cust.txt
│   ├── movies.txt
│   ├── ratings_1.txt
│   ├── ratings_2.txt
│   └── users.txt
└── lab1_java_sources/
    ├── TransAnalysis1.java
    ├── TransAnalysis2.java
    ├── TransAnalysis3.java
    ├── TransAnalysis4.java
    ├── TransAnalysis5.java
    ├── TransAnalysis6.java
    ├── MovieRatingAverage.java
    ├── GenreRatingAverage.java
    └── GenderRatingAverage.java
```

---

## 2. Đưa file từ Windows vào Cloudera

Copy hai thư mục `data` và `lab1_java_sources` vào:

```text
/home/cloudera/Lab01/
```

Cấu trúc local:

```text
/home/cloudera/Lab01/
├── data/
└── lab1_java_sources/
```

Kiểm tra:

```bash
cd /home/cloudera/Lab01
ls
ls /home/cloudera/Lab01/data
ls /home/cloudera/Lab01/lab1_java_sources
```

---

## 3. Tạo thư mục HDFS

```bash
hdfs dfs -mkdir -p /user/cloudera/lab1/trans
hdfs dfs -mkdir -p /user/cloudera/lab1/ml
hdfs dfs -mkdir -p /mycache
```

---

## 4. Đưa dữ liệu lên HDFS

### Phần B

```bash
hdfs dfs -put -f /home/cloudera/Lab01/data/trans.txt /user/cloudera/lab1/trans/
hdfs dfs -put -f /home/cloudera/Lab01/data/cust.txt /mycache/cust
```

### Phần C

```bash
hdfs dfs -put -f /home/cloudera/Lab01/data/movies.txt /user/cloudera/lab1/ml/
hdfs dfs -put -f /home/cloudera/Lab01/data/ratings_1.txt /user/cloudera/lab1/ml/
hdfs dfs -put -f /home/cloudera/Lab01/data/ratings_2.txt /user/cloudera/lab1/ml/
hdfs dfs -put -f /home/cloudera/Lab01/data/users.txt /user/cloudera/lab1/ml/
```

---

## 5. Kiểm tra dữ liệu HDFS

```bash
hdfs dfs -ls -R /user/cloudera/lab1
hdfs dfs -ls /mycache
hdfs dfs -cat /mycache/cust
hdfs fsck /mycache/cust
```

Các đường dẫn cần có:

```text
/user/cloudera/lab1/trans/trans.txt
/user/cloudera/lab1/ml/movies.txt
/user/cloudera/lab1/ml/ratings_1.txt
/user/cloudera/lab1/ml/ratings_2.txt
/user/cloudera/lab1/ml/users.txt
/mycache/cust
```

Nếu `fsck` báo:

```text
The filesystem under path '/mycache/cust' is HEALTHY
```

thì file cache dùng được.

---

## 6. Tạo project trong Eclipse

Mở Eclipse:

```text
File → New → Java Project
```

Tên project:

```text
Lab01
```

Project Eclipse nằm ở:

```text
/home/cloudera/workspace/Lab01/
```

Đây là thư mục khác với thư mục chứa file đã copy từ Windows:

```text
/home/cloudera/Lab01/
```

Điều này hoàn toàn bình thường.

---

## 7. Import 9 file Java

Trong Eclipse:

```text
File → Import → General → File System
```

Chọn:

```text
/home/cloudera/Lab01/lab1_java_sources
```

Import vào:

```text
Lab01/src
```

Trong `(default package)` cần có đủ 9 file Java.

---

## 8. Thêm Hadoop libraries

Nếu các import Hadoop bị lỗi đỏ:

```text
Project
→ Build Path
→ Configure Build Path
→ Libraries
→ Add External JARs
```

Thêm các JAR trong:

```text
/usr/lib/hadoop/client
```

Nếu vẫn thiếu, kiểm tra thêm:

```text
/usr/lib/hadoop
```

Không được còn dấu `X` đỏ trước khi export JAR.

---

## 9. Sửa cảnh báo `Job` deprecated

Nếu có dòng:

```java
Job job = new Job(conf, "...");
```

đổi thành:

```java
Job job = Job.getInstance(conf, "...");
```

Ví dụ:

```java
Configuration conf = new Configuration();
Job job = Job.getInstance(conf, "Gender rating average");
```

Có thể dùng:

```text
Ctrl + Shift + O
```

để Eclipse tự organize imports.

---

## 10. Clean project

```text
Project → Clean... → Lab01 → Clean
```

Đảm bảo project không còn lỗi đỏ.

---

## 11. Export JAR

Chuột phải project:

```text
Lab01 → Export → Java → JAR file
```

Chọn:

```text
Lab01
└── src
    └── (default package)
```

Bật:

```text
Export generated class files and resources
Compress the contents of the JAR file
```

Có thể bỏ chọn:

```text
.classpath
.project
```

Đường dẫn JAR:

```text
/home/cloudera/Lab01/lab1.jar
```

Nhấn `Finish`.

---

## 12. Kiểm tra JAR

```bash
ls -lh /home/cloudera/Lab01/lab1.jar
```

Kiểm tra phần B:

```bash
jar tf /home/cloudera/Lab01/lab1.jar | grep TransAnalysis
```

Cần thấy `TransAnalysis1` đến `TransAnalysis6`.

Kiểm tra phần C:

```bash
jar tf /home/cloudera/Lab01/lab1.jar | grep RatingAverage
```

Cần thấy:

```text
MovieRatingAverage
GenreRatingAverage
GenderRatingAverage
```

---

# PHẦN B

Quy trình mỗi bài:

```text
1. Xóa output cũ
2. Chạy hadoop jar
3. Chờ "completed successfully"
4. Dùng hdfs dfs -cat để xem kết quả
```

Output của Hadoop không được tồn tại trước khi job chạy.

---

## 13. B.1 – TransAnalysis1

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/out1
hadoop jar /home/cloudera/Lab01/lab1.jar TransAnalysis1 /user/cloudera/lab1/trans /user/cloudera/lab1/out1
hdfs dfs -cat /user/cloudera/lab1/out1/part-r-00000
```

---

## 14. B.2 – TransAnalysis2

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/out2
hadoop jar /home/cloudera/Lab01/lab1.jar TransAnalysis2 /user/cloudera/lab1/trans /user/cloudera/lab1/out2
hdfs dfs -cat /user/cloudera/lab1/out2/part-r-00000
```

---

## 15. B.3 – TransAnalysis3

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/out3
hadoop jar /home/cloudera/Lab01/lab1.jar TransAnalysis3 /user/cloudera/lab1/trans /user/cloudera/lab1/out3
hdfs dfs -cat /user/cloudera/lab1/out3/part-r-00000
```

---

## 16. B.4 – TransAnalysis4

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/out4
hadoop jar /home/cloudera/Lab01/lab1.jar TransAnalysis4 /user/cloudera/lab1/trans /user/cloudera/lab1/out4
hdfs dfs -cat /user/cloudera/lab1/out4/part-r-00000
```

---

## 17. B.5 – TransAnalysis5

Bài này dùng:

```text
/mycache/cust
```

Có thể kiểm tra trước:

```bash
hdfs dfs -ls /mycache/cust
```

Sau đó chạy:

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/out5
hadoop jar /home/cloudera/Lab01/lab1.jar TransAnalysis5 /user/cloudera/lab1/trans /user/cloudera/lab1/out5
hdfs dfs -cat /user/cloudera/lab1/out5/part-r-00000
```

---

## 18. B.6 – TransAnalysis6

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/out6
hadoop jar /home/cloudera/Lab01/lab1.jar TransAnalysis6 /user/cloudera/lab1/trans /user/cloudera/lab1/out6
hdfs dfs -cat /user/cloudera/lab1/out6/part-r-00000
```

Với mapper tạo giá trị:

```text
id,name,age,amount
```

reducer phải lấy `parts[3]` làm amount.

---

# PHẦN C.1

Dữ liệu:

```text
/user/cloudera/lab1/ml/movies.txt
/user/cloudera/lab1/ml/ratings_1.txt
/user/cloudera/lab1/ml/ratings_2.txt
/user/cloudera/lab1/ml/users.txt
```

---

## 19. C.1 – Bài 1: MovieRatingAverage

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/c1_bai1
hadoop jar /home/cloudera/Lab01/lab1.jar MovieRatingAverage /user/cloudera/lab1/ml/ratings_1.txt /user/cloudera/lab1/ml/ratings_2.txt /user/cloudera/lab1/c1_bai1
hdfs dfs -cat /user/cloudera/lab1/c1_bai1/part-r-00000
```

Kết quả phải có điểm trung bình, số lượt đánh giá của từng phim và phim có điểm cao nhất.

Với bộ dữ liệu đã dùng, phim cao nhất là:

```text
Avatar (2009) – 4.75
```

---

## 20. C.1 – Bài 2: GenreRatingAverage

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/c1_bai2
hadoop jar /home/cloudera/Lab01/lab1.jar GenreRatingAverage /user/cloudera/lab1/ml/ratings_1.txt /user/cloudera/lab1/ml/ratings_2.txt /user/cloudera/lab1/c1_bai2
hdfs dfs -cat /user/cloudera/lab1/c1_bai2/part-r-00000
```

Bài này tính điểm trung bình và số lượt đánh giá theo thể loại. Một phim có nhiều thể loại thì rating của phim được tính cho từng thể loại tương ứng.

---

## 21. C.1 – Bài 3: GenderRatingAverage

Thứ tự tham số:

```text
args[0] = movies.txt
args[1] = ratings_1.txt
args[2] = ratings_2.txt
args[3] = output
```

Chạy:

```bash
hdfs dfs -rm -r -f /user/cloudera/lab1/c1_bai3
hadoop jar /home/cloudera/Lab01/lab1.jar GenderRatingAverage /user/cloudera/lab1/ml/movies.txt /user/cloudera/lab1/ml/ratings_1.txt /user/cloudera/lab1/ml/ratings_2.txt /user/cloudera/lab1/c1_bai3
hdfs dfs -cat /user/cloudera/lab1/c1_bai3/part-r-00000
```

Bài này dùng reduce-side join cho `movies.txt` và ratings, còn `users.txt` được dùng qua Distributed Cache để tra giới tính.

Nếu một phim thiếu đánh giá của một giới thì có thể hiện `N/A`. Tuy nhiên với chính bộ dữ liệu mẫu đã dùng trong Lab này, mỗi phim đều có một đánh giá nam và một đánh giá nữ nên không có `N/A`.

---

## 22. Chụp ảnh báo cáo

Mỗi bài nên có 2 ảnh.

Ảnh 1:

```text
lệnh hadoop jar
...
INFO mapreduce.Job: Job ... completed successfully
```

Không cần giữ phần log dài sau:

```text
Counters: ...
```

Ảnh 2:

```text
hdfs dfs -cat .../part-r-00000
```

và toàn bộ kết quả phía dưới.

---

## 23. Các bài đưa vào báo cáo

Phần B:

```text
B.1
B.2
B.3
B.4
B.5
B.6
```

Phần C.1:

```text
C.1 - Bài 1
C.1 - Bài 2
C.1 - Bài 3
```

Có thể trình bày:

```text
B.1. TransAnalysis1
[Ảnh hadoop jar]
[Ảnh hdfs dfs -cat]

B.2. TransAnalysis2
[Ảnh hadoop jar]
[Ảnh hdfs dfs -cat]

...

C.1 - Bài 1. MovieRatingAverage
[Ảnh hadoop jar]
[Ảnh hdfs dfs -cat]

C.1 - Bài 2. GenreRatingAverage
[Ảnh hadoop jar]
[Ảnh hdfs dfs -cat]

C.1 - Bài 3. GenderRatingAverage
[Ảnh hadoop jar]
[Ảnh hdfs dfs -cat]
```

---

## 24. Yêu cầu nộp bài

Theo tài liệu Lab:

- C.1 bắt buộc.
- C.2 tùy chọn.
- Nộp một file ZIP:

```text
<MSSV>-Lab1.zip
```

Bên trong gồm:

```text
các file .java của từng bài
file báo cáo PDF
```

PDF cần có:

```text
ảnh lệnh hadoop jar
ảnh kết quả hdfs dfs -cat
```

---

## 25. Cấu trúc cuối cùng đề xuất

Local:

```text
/home/cloudera/Lab01/
├── data/
├── lab1_java_sources/
└── lab1.jar
```

Eclipse project:

```text
/home/cloudera/workspace/Lab01/
```

HDFS:

```text
/user/cloudera/lab1/
├── trans/
│   └── trans.txt
├── ml/
│   ├── movies.txt
│   ├── ratings_1.txt
│   ├── ratings_2.txt
│   └── users.txt
├── out1/
├── out2/
├── out3/
├── out4/
├── out5/
├── out6/
├── c1_bai1/
├── c1_bai2/
└── c1_bai3/
```

Cache:

```text
/mycache/cust
```

JAR:

```text
/home/cloudera/Lab01/lab1.jar
```
