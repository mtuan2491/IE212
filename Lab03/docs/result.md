# Kết quả bài tập về nhà Lab03 – Fecom với Spark DataFrame

Số liệu lấy từ **output đã lưu** trong [Lab03_BTVN.ipynb](../src/Lab03_BTVN.ipynb). Năm CSV đi kèm được kiểm tra số bản ghi bằng CSV parser, phân cách `;`, hỗ trợ trường nhiều dòng; kết quả khớp Bài 1. Không chạy lại notebook trong quá trình soạn tài liệu.

**Quy ước:** đơn hàng đếm theo Orders; khách đã mua đếm `Subscriber_ID` phân biệt có giao dịch; lượt bán là số dòng Order_Items. Doanh thu bằng **`Price + Freight_Value`**, không lọc trạng thái đơn, chưa xác nhận đơn vị tiền. Số thập phân trong tài liệu dùng dấu phẩy, dấu chấm phân cách hàng nghìn.

## Mục lục

- [Bài 1. Đọc dữ liệu và kiểm tra lược đồ](#bài-1-đọc-dữ-liệu-và-kiểm-tra-lược-đồ)
- [Bài 2. Tổng số đơn hàng, khách hàng và người bán](#bài-2-tổng-số-đơn-hàng-khách-hàng-và-người-bán)
- [Bài 3. Số đơn hàng theo quốc gia](#bài-3-số-đơn-hàng-theo-quốc-gia)
- [Bài 4. Số đơn hàng theo năm và tháng](#bài-4-số-đơn-hàng-theo-năm-và-tháng)
- [Bài 5. Điểm đánh giá trung bình và phân bố](#bài-5-điểm-đánh-giá-trung-bình-và-phân-bố)
- [Bài 6. Xếp hạng người bán](#bài-6-xếp-hạng-người-bán)
- [Bài 7. Doanh thu năm 2024 theo danh mục](#bài-7-doanh-thu-năm-2024-theo-danh-mục)
- [Bài 8. Sản phẩm bán chạy và điểm trung bình](#bài-8-sản-phẩm-bán-chạy-và-điểm-trung-bình)
- [Phần D – So sánh các mô hình xử lý](#phần-d--so-sánh-các-mô-hình-xử-lý)

## Bài 1. Đọc dữ liệu và kiểm tra lược đồ

**Mục tiêu:** xác nhận dữ liệu, kiểu cột và các khóa trước khi tổng hợp/nối bảng.

**Phương pháp:** `spark.read` với header, `sep=";"`, UTF-8, `inferSchema=True`, `FAILFAST`; reviews dùng thêm `multiLine=True`, `escape='"'`. In schema, so số dòng với mốc, chuẩn hóa thời gian và kiểm tra khóa bằng assertion.

| Bảng | Số dòng | Số cột |
| --- | ---: | ---: |
| Orders | 99.441 | 8 |
| Order_Items | 112.650 | 7 |
| Products | 32.951 | 6 |
| Customer_List | 102.727 | 10 |
| Order_Reviews | 99.223 | 7 |

Output suy ra timestamp ở Orders, Shipping_Limit_Date và thời gian reviews; Customer_List có Subscribe_Date/First_Order_Date kiểu date. Price/Freight_Value ban đầu là double; Review_Score và Order_Item_ID là int. Cell tiếp theo chuẩn hóa các mốc thời gian về timestamp. Hai bảng kiểm tra cột string và lỗi parse không có dòng, vì các cột thời gian đã được suy ra date/timestamp.

Các assertion kiểm tra Orders duy nhất theo Order_ID, Products duy nhất theo Product_ID; bảng tra khách duy nhất theo Customer_Trx_ID không NULL và có Subscriber_ID. Không có output loại lỗi ở hai cell Bài 1.

## Bài 2. Tổng số đơn hàng, khách hàng và người bán

**Mục tiêu:** thống kê quy mô hoạt động và phân biệt người đăng ký với người đã mua.

**Phương pháp:** `count("*")` cho Orders; `left_semi` bảng tra khách với khóa có trong Orders rồi `countDistinct("Subscriber_ID")`; `countDistinct("Seller_ID")` trên items.

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Đơn hàng | 99.441 |
| Khách hàng đã mua | 96.096 |
| Người bán | 3.095 |
| Dòng đăng ký trong Customer_List | 102.727 |
| Dòng đăng ký chưa có Customer_Trx_ID | 3.286 |

Không dùng số dòng Customer_List hoặc số khóa giao dịch làm số người mua phân biệt.

## Bài 3. Số đơn hàng theo quốc gia

**Mục tiêu:** đếm đơn theo Customer_Country.

**Phương pháp:** left join Orders với bảng tra khách theo Customer_Trx_ID, kiểm tra số dòng/khóa đơn và khách không khớp, sau đó `groupBy().agg(count)`.

| Kiểm tra | Kết quả |
| --- | ---: |
| Dòng sau join | 99.441 |
| Order_ID phân biệt sau join | 99.441 |
| Đơn không khớp khách | 0 |
| Quốc gia | 27 |
| Tổng đơn qua các quốc gia | 99.441 |

| Quốc gia | Đơn hàng |
| --- | ---: |
| Germany | 41.754 |
| France | 12.848 |
| Netherlands | 11.629 |
| Belgium | 5.464 |
| Austria | 5.043 |
| Switzerland | 3.640 |
| United Kingdom | 3.382 |
| Poland | 2.139 |
| Czechia | 2.034 |
| Italy | 2.025 |

Germany dẫn đầu. Bảng trên là top-10 trong 27 quốc gia; tổng 99.441 lấy từ bảng kiểm tra tổng, không phải tổng riêng top-10.

## Bài 4. Số đơn hàng theo năm và tháng

**Mục tiêu:** thống kê đơn theo thời điểm mua.

**Phương pháp:** kiểm tra thời điểm mua không NULL, lấy `year`/`month`, gộp rồi sắp năm tăng và tháng giảm. Output có **25 nhóm năm–tháng có đơn**, không tự bổ sung tháng thiếu bằng 0.

| Năm | Tháng | Đơn hàng |
| --- | ---: | ---: |
| 2022 | 12 | 1 |
| 2022 | 10 | 324 |
| 2022 | 9 | 4 |
| 2023 | 12 | 5.673 |
| 2023 | 11 | 7.544 |
| 2023 | 10 | 4.631 |
| 2023 | 9 | 4.285 |
| 2023 | 8 | 4.331 |
| 2023 | 7 | 4.026 |
| 2023 | 6 | 3.245 |
| 2023 | 5 | 3.700 |
| 2023 | 4 | 2.404 |
| 2023 | 3 | 2.682 |
| 2023 | 2 | 1.780 |
| 2023 | 1 | 800 |
| 2024 | 10 | 4 |
| 2024 | 9 | 16 |
| 2024 | 8 | 6.512 |
| 2024 | 7 | 6.292 |
| 2024 | 6 | 6.167 |
| 2024 | 5 | 6.873 |
| 2024 | 4 | 6.939 |
| 2024 | 3 | 7.211 |
| 2024 | 2 | 6.728 |
| 2024 | 1 | 7.269 |

Khoảng thời gian đã lưu: **2022-09-04 21:15:00 → 2024-10-17 17:30:00**, múi giờ phiên Spark UTC. Assertion xác nhận tổng nhóm bằng 99.441 đơn. Không diễn giải tháng biên hoặc tháng không có bản ghi như dữ liệu đầy đủ của cả năm.

## Bài 5. Điểm đánh giá trung bình và phân bố

**Mục tiêu:** kiểm tra miền giá trị, phân bố và điểm trung bình.

**Phương pháp:** đếm điểm NULL/không hợp lệ trước khi `groupBy("Review_Score")`; dùng `round(avg(...), 2)` cho trung bình. Không loại bản ghi để đạt mốc.

| Điểm | Số đánh giá |
| --- | ---: |
| 1 | 11.424 |
| 2 | 3.151 |
| 3 | 8.179 |
| 4 | 19.141 |
| 5 | 57.328 |
| Tổng | 99.223 |

Output kiểm tra **0 NULL, 0 điểm không hợp lệ**. Trung bình **4,09** trên 99.223 bản ghi đánh giá, không phải trung bình sau khi gộp mỗi đơn thành một điểm.

## Bài 6. Xếp hạng người bán

**Mục tiêu:** xếp hạng theo tổng giá trị dòng hàng.

**Phương pháp:** cast Price/Freight_Value sang `decimal(20,2)`, cộng hai cột, gộp theo Seller_ID để tính doanh thu và số Order_ID phân biệt. Dùng `rank()` trên cửa sổ doanh thu giảm dần; Seller_ID là khóa phụ khi hiển thị.

| Hạng | Seller_ID hiển thị trong output | Doanh thu | Số đơn |
| --- | --- | ---: | ---: |
| 1 | `4869f7a5dfa277a7d...` | 249.640,70 | 1.132 |
| 2 | `7c67e1448b00f6e96...` | 239.536,44 | 982 |
| 3 | `53243585a1d6dc264...` | 235.856,68 | 358 |
| 4 | `4a3ca9315b744ce9f...` | 235.539,96 | 1.806 |
| 5 | `fa1c13f2614d7b5c4...` | 204.084,73 | 585 |

Bảng xếp hạng có **3.095 người bán**. Mã trong tài liệu giữ dấu `...` do `.show()` cắt hiển thị, không dùng chuỗi này làm khóa nối. `rank` cho cùng hạng khi bằng doanh thu và có thể bỏ hạng kế tiếp; số đơn được đếm phân biệt trong từng người bán.

## Bài 7. Doanh thu năm 2024 theo danh mục

**Mục tiêu:** phân tích doanh thu theo danh mục trên các đơn mua năm 2024.

**Phương pháp:** lọc Orders theo năm mua 2024, inner join items theo Order_ID; kiểm tra sản phẩm không thiếu, left join danh mục và xác nhận không đổi số dòng; tổng hợp giá trị dòng theo Product_Category_Name.

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Dòng hàng năm 2024 | 61.416 |
| Nhóm danh mục | 71 |
| Tổng doanh thu dòng hàng | 8.643.697,60 |
| Tổng doanh thu qua các nhóm danh mục | 8.643.697,60 |

| Danh mục dẫn đầu | Doanh thu |
| --- | ---: |
| Health_Beauty | 885.191,12 |
| Watches_Gifts | 771.986,75 |
| Bed_Bath_Table | 650.794,70 |
| Sports_Leisure | 621.999,34 |
| Computers_Accessories | 594.771,04 |

71 nhóm **bao gồm giá trị `#N/A`** với doanh thu **90.849,48**; không gọi đây là 71 danh mục đã chuẩn hóa đầy đủ. Notebook in toàn bộ 71 nhóm và dùng assertion so tổng doanh thu trước/sau gộp. Không lọc đơn hủy hoặc chỉ giữ đơn delivered.

## Bài 8. Sản phẩm bán chạy và điểm trung bình

**Mục tiêu:** lấy sản phẩm có nhiều dòng hàng nhất và điểm đánh giá tương ứng, tránh nhân dòng khi nối reviews.

**Phương pháp:** gộp reviews theo Order_ID thành `diem_don`, left join items với bảng đã gộp, đếm dòng theo Product_ID, lấy `avg(diem_don)` và số dòng có điểm. Nối danh mục rồi sắp lượt bán giảm dần/mã sản phẩm tăng dần.

| Kiểm tra đánh giá theo đơn | Kết quả |
| --- | ---: |
| Đơn có nhiều hơn một đánh giá | 547 |
| Dòng đánh giá dư so với một dòng mỗi đơn | 551 |
| Đơn không có đánh giá | 769 |

Nhãn output `so_dong_tang_neu_noi_truc_tiep` là tổng số đánh giá dư ở cấp **đơn**; không đồng nhất 551 với số dòng items sẽ tăng khi nối trực tiếp, vì một đơn có thể có nhiều dòng hàng. Assertion của bản đã gộp xác nhận phép nối vẫn giữ **112.650 dòng items**.

| Product_ID hiển thị | Danh mục | Lượt bán | Điểm TB | Dòng hàng có đánh giá |
| --- | --- | ---: | ---: | ---: |
| `aca2eb7d00ea1a7b8...` | Furniture_Decor | 527 | 4,02 | 524 |
| `99a4788cb24856965...` | Bed_Bath_Table | 488 | 3,90 | 479 |
| `422879e10f4668299...` | Garden_Tools | 484 | 3,96 | 483 |
| `389d119b48cf3043d...` | Garden_Tools | 392 | 4,12 | 391 |
| `368c6c730842d7801...` | Garden_Tools | 388 | 3,92 | 385 |

Sản phẩm đầu có **527 lượt bán**, trong đó 524 dòng hàng có điểm đơn; điểm trung bình **4,02**. Đây là trung bình điểm đơn gắn vào các dòng hàng của sản phẩm; đơn nhiều đánh giá đã được lấy trung bình trước, NULL không tính vào `avg`. Không mô tả đây là điểm đánh giá riêng trực tiếp cho sản phẩm hoặc số đơn phân biệt. Mã sản phẩm bị cắt khi hiển thị được giữ nguyên như output.

## Phần D – So sánh các mô hình xử lý

Xem [báo cáo PDF](../report/BaoCao.pdf) cho phần so sánh Hadoop MapReduce, Spark RDD và Spark DataFrame/Spark SQL. Phần này không bổ sung vào notebook BTVN.

Bài 1–6 bắt buộc và Bài 7–8 tự chọn đều đã có output; toàn bộ các mốc đối chiếu chính khớp bản lưu. Xem [hướng dẫn BTVN](Huong_dan_Lab3_BTVN.md) để chạy lại trên bản sao và [hướng dẫn thực hành](Huong_dan_Lab3_Thuc_Hanh.md#5-kết-quả-mong-đợi) cho kết quả MovieLens riêng.
