# IE212 – Công nghệ dữ liệu lớn

Repository lưu mã nguồn, dữ liệu thực hành, hướng dẫn và báo cáo của môn **IE212 – Công nghệ dữ liệu lớn**. Các bài Lab hiện có sử dụng Hadoop MapReduce với Java, Apache Spark RDD và Spark DataFrame/Spark SQL với Python để xử lý dữ liệu.

## Các bài thực hành

| Bài | Nội dung đã thực hiện | Tài liệu |
| --- | --- | --- |
| Lab01 | Hadoop, HDFS, MapReduce: 6 bài phân tích giao dịch và 3 bài phân tích đánh giá phim bằng Java | [README Lab01](Lab01/README.md) |
| Lab02 | Thực hành Spark RDD, TransAnalysis, MovieLens; BTVN gồm 7 bài phân tích OpenFlights | [README Lab02](Lab02/README.md) |
| Lab03 | Thực hành Spark DataFrame, Spark SQL, join và Window với MovieLens mini; BTVN gồm 8 bài phân tích Fecom | [README Lab03](Lab03/README.md) |

## Cấu trúc repository

```text
.
├── README.md
├── Lab01/
│   ├── README.md
│   ├── data/
│   │   ├── README.md
│   │   ├── trans/
│   │   └── movielens/
│   ├── src/                         # 9 chương trình Java
│   ├── docs/
│   │   ├── Huong_dan_Lab1_Hadoop_MapReduce.md
│   │   └── screenshots/
│   └── report/
│       └── 23521720_Lab_1.pdf
├── Lab02/
│   ├── README.md
│   ├── data/
│   │   ├── openflights/             # 5 file .dat
│   │   ├── trans/
│   │   └── movielens-mini/
│   ├── src/
│   │   ├── Lab02_ThucHanh.ipynb
│   │   └── Lab02_BTVN.ipynb
│   ├── docs/
│   │   ├── Huong_dan_Lab2_Thuc_Hanh.md
│   │   ├── Huong_dan_Lab2_BTVN.md
│   │   └── result.md
│   └── report/
│       └── BaoCao.pdf
└── Lab03/
    ├── README.md
    ├── data/
    │   ├── fecom/                   # 5 file .csv
    │   └── movielens-mini/          # 5 file .txt
    ├── src/
    │   ├── Lab03_ThucHanh.ipynb
    │   └── Lab03_BTVN.ipynb
    ├── docs/
    │   ├── Huong_dan_Lab3_Thuc_Hanh.md
    │   ├── Huong_dan_Lab3_BTVN.md
    │   └── result.md
    └── report/
        └── BaoCao.pdf
```

Lab02 có hai nội dung độc lập: thực hành trên lớp dùng `data/trans/` và `data/movielens-mini/` để học Spark RDD, TransAnalysis và MovieLens; BTVN dùng `data/openflights/` để phân tích mạng bay. Xem [README Lab02](Lab02/README.md) để chọn notebook và tài liệu tương ứng.

Lab03 chuyển sang Spark DataFrame/Spark SQL: thực hành dùng MovieLens mini, BTVN dùng Fecom. Xem [README Lab03](Lab03/README.md) để chuẩn bị dữ liệu và chọn tài liệu tương ứng.

## Môi trường và công nghệ

| Phạm vi | Công nghệ/môi trường có căn cứ trong repository |
| --- | --- |
| Lab01 | Java, Hadoop, HDFS, MapReduce, Distributed Cache; tài liệu ghi nhận Cloudera QuickStart VM, Eclipse và VMware. Chưa có thông tin phiên bản cụ thể. |
| Lab02 | Python, PySpark, Spark RDD; hai notebook có mã upload Google Colab và chạy Spark bằng `local[*]`. |
| Phiên bản Lab02 | Thực hành cài `pyspark==3.5.1` và in Spark `3.5.1`. BTVN cài bản này khi thiếu PySpark, metadata khai báo Python `3.10`. Chưa có output xác nhận Python/Java của hai runtime và PySpark thực tế của BTVN. |
| Lab03 | Python, PySpark, DataFrame, Spark SQL và Window; hai notebook cài và in Spark `3.5.1`, chọn/cài Java 17 trên Colab, dùng `local[*]`, UTC và 8 shuffle partition. Chưa có output xác nhận phiên bản Python/Java runtime gốc. |

## Bắt đầu

- **Lab01:** xem [nội dung bài thực hành](Lab01/README.md), [dữ liệu](Lab01/data/README.md) và [hướng dẫn chạy Hadoop MapReduce](Lab01/docs/Huong_dan_Lab1_Hadoop_MapReduce.md).
- **Lab02:** xem [tổng quan hai nội dung](Lab02/README.md). Chọn [hướng dẫn thực hành RDD, TransAnalysis và MovieLens](Lab02/docs/Huong_dan_Lab2_Thuc_Hanh.md), hoặc [hướng dẫn BTVN OpenFlights](Lab02/docs/Huong_dan_Lab2_BTVN.md) và [kết quả BTVN Bài 1–7](Lab02/docs/result.md).
- **Lab03:** xem [tổng quan DataFrame và Spark SQL](Lab03/README.md). Chọn [hướng dẫn thực hành MovieLens](Lab03/docs/Huong_dan_Lab3_Thuc_Hanh.md), hoặc [hướng dẫn BTVN Fecom](Lab03/docs/Huong_dan_Lab3_BTVN.md) và [kết quả BTVN Bài 1–8](Lab03/docs/result.md). Cả hai notebook giữ output; cell upload đầu yêu cầu `data.zip` chứa cả hai bộ dữ liệu.

Cả hai notebook Lab02 đã lưu output. Giữ nguyên dữ liệu đi kèm khi chạy lại để có cùng cơ sở đối chiếu; dữ liệu tải mới từ nguồn có thể khác bản trong repository.

## Tài liệu tham khảo

- [Apache Hadoop – MapReduce Tutorial](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html) — tài liệu framework, không dùng để suy ra phiên bản Hadoop của Lab01.
- [Apache Spark 3.5.1](https://archive.apache.org/dist/spark/docs/3.5.1/) và [RDD Programming Guide](https://archive.apache.org/dist/spark/docs/3.5.1/rdd-programming-guide.html).
- [OpenFlights – mô tả dữ liệu và điều kiện sử dụng](https://openflights.org/data.php). Xem thêm [ghi nhận nguồn dữ liệu Lab02](Lab02/README.md#nguồn-và-điều-kiện-sử-dụng).

Các file biên dịch `.class`, `.jar`, metadata Eclipse và file tạm không cần đưa lên GitHub nếu không phục vụ việc tái hiện bài thực hành. Hướng dẫn riêng và báo cáo được đặt trong từng Lab.
