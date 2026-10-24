# Kết quả bài tập về nhà Lab02 – OpenFlights với Spark RDD

Số liệu lấy từ output đã lưu trong [notebook](../src/Lab02_BTVN.ipynb), đối chiếu với phương pháp, ảnh kết quả và nhận xét trong [báo cáo PDF](../report/BaoCao.pdf). Số dòng của 5 file dữ liệu được kiểm tra trực tiếp trong repository. Đây là kết quả của bản dữ liệu đi kèm, không phải số liệu hoạt động hàng không hiện tại.

**Quy ước:** “đường bay” là một bản ghi trong `routes.dat`; notebook không gộp các hãng trên cùng cặp sân bay thành một đường bay duy nhất và không đo tần suất chuyến bay. Quốc gia/vùng lãnh thổ được giữ theo chuỗi trong `airports.dat`. Mọi phép tra sân bay dùng bảng IATA có đúng 3 ký tự chữ theo `len(p[4]) == 3 and p[4].isalpha()`.

## Mục lục

- [Bài 1. Đọc dữ liệu và kiểm tra](#bài-1-đọc-dữ-liệu-và-kiểm-tra)
- [Bài 2. Sân bay bận rộn nhất](#bài-2-sân-bay-bận-rộn-nhất)
- [Bài 3. Số hãng bay khai thác mỗi sân bay](#bài-3-số-hãng-bay-khai-thác-mỗi-sân-bay)
- [Bài 4. Thống kê theo loại máy bay](#bài-4-thống-kê-theo-loại-máy-bay)
- [Bài 5. Số đường bay theo quốc gia](#bài-5-số-đường-bay-theo-quốc-gia)
- [Bài 6. Mạng bay Việt Nam](#bài-6-mạng-bay-việt-nam)
- [Bài 7. Nội địa so với quốc tế trên toàn thế giới](#bài-7-nội-địa-so-với-quốc-tế-trên-toàn-thế-giới)

## Bài 1. Đọc dữ liệu và kiểm tra

**Mục tiêu:** kiểm tra quy mô và cách tách dữ liệu, chuẩn bị bảng tra cho các bài sau.

**Phương pháp:** đọc ba file bằng `sc.textFile()`, dùng `split(',')` cho routes và `csv.reader()` cho airports/airlines. Dùng `count()`, `first()`, `filter()` để kiểm tra; dùng `collectAsMap()`, `sc.broadcast()` tạo và phân phối bảng tra sân bay/hãng.

| RDD | Số dòng | Số cột |
| --- | ---: | ---: |
| routes | 67.663 | 9 |
| airports | 7.698 | 14 |
| airlines | 6.162 | 8 |

| Kiểm tra bổ sung | Kết quả |
| --- | ---: |
| Sân bay có IATA hợp lệ theo điều kiện notebook | 6.071 |
| Tên sân bay chứa dấu phẩy | 16 |

Notebook in số cột từ bản ghi đầu tiên. Dùng CSV parser cho sân bay/hãng để giữ nguyên các trường được đặt trong dấu nháy kép và có dấu phẩy bên trong.

Hai file còn lại có **246 dòng** (`planes.dat`) và **261 dòng** (`countries.dat`), được đếm trực tiếp khi kiểm tra repository; đây không phải output của Bài 1. Notebook upload cả 5 file nhưng chỉ đọc 3 file vào RDD.

## Bài 2. Sân bay bận rộn nhất

**Mục tiêu:** thống kê đường bay đi/đến và tìm sân bay có nhiều đường bay đi nhất.

**Phương pháp:** `map()` tạo cặp (mã sân bay, 1), `reduceByKey(add)` đếm theo từng đầu đường bay; `takeOrdered(10, key=lambda x: (-x[1], x[0]))` xếp hạng số đường bay đi giảm dần, mã sân bay tăng dần khi bằng nhau.

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Mã sân bay có đường bay đi | 3.409 |
| Mã sân bay có đường bay đến | 3.418 |
| Tổng số bản ghi tính theo sân bay đi | 67.663 |
| Tổng số bản ghi tính theo sân bay đến | 67.663 |

| IATA | Đường bay đi | Thành phố | Quốc gia |
| --- | ---: | --- | --- |
| ATL | 915 | Atlanta | United States |
| ORD | 558 | Chicago | United States |
| PEK | 535 | Beijing | China |
| LHR | 527 | London | United Kingdom |
| CDG | 524 | Paris | France |
| FRA | 497 | Frankfurt | Germany |
| LAX | 492 | Los Angeles | United States |
| DFW | 469 | Dallas-Fort Worth | United States |
| JFK | 456 | New York | United States |
| AMS | 453 | Amsterdam | Netherlands |

ATL dẫn đầu theo tiêu chí số bản ghi đường bay đi. Tập mã xuất hiện ở đầu đi và đầu đến không hoàn toàn giống nhau, nên hai số lượng mã sân bay khác nhau.

## Bài 3. Số hãng bay khai thác mỗi sân bay

**Mục tiêu:** đếm số mã hãng phân biệt có đường bay xuất phát từ mỗi sân bay.

**Phương pháp:** lấy cặp `(p[2], p[0])` tức sân bay đi–mã hãng trong routes, gọi `distinct()`, rồi `map()` và `reduceByKey(add)`. Dùng `takeOrdered()` lấy 10 sân bay dẫn đầu; tra thêm số đường bay đi từ Bài 2.

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Cặp sân bay đi–mã hãng phân biệt | 19.288 |
| Sân bay chỉ có một mã hãng | 1.313 |
| Số mã hãng tại ATL | 37 |

| IATA | Số hãng | Đường bay đi | Thành phố | Quốc gia/vùng lãnh thổ |
| --- | ---: | ---: | --- | --- |
| CDG | 108 | 524 | Paris | France |
| FRA | 100 | 497 | Frankfurt | Germany |
| BKK | 98 | 326 | Bangkok | Thailand |
| FCO | 92 | 331 | Rome | Italy |
| LHR | 86 | 527 | London | United Kingdom |
| DXB | 84 | 356 | Dubai | United Arab Emirates |
| HKG | 83 | 355 | Hong Kong | Hong Kong |
| SIN | 83 | 408 | Singapore | Singapore |
| PEK | 81 | 535 | Beijing | China |
| AMS | 79 | 453 | Amsterdam | Netherlands |

CDG có nhiều mã hãng nhất. ATL có 915 đường bay đi nhưng chỉ có 37 hãng, nên không nằm trong bảng này. “Khai thác” ở đây theo mã hãng có trong bản ghi; notebook không lọc cột codeshare.

## Bài 4. Thống kê theo loại máy bay

**Mục tiêu:** đếm số bản ghi đường bay gắn với từng mã loại máy bay.

**Phương pháp:** dùng `filter()` kiểm tra Equipment rỗng; `flatMap()` tách từng mã theo khoảng trắng từ `p[8]`, sau đó `reduceByKey(add)`. Mỗi bản ghi có nhiều mã đóng góp vào nhiều nhóm; không tra tên từ `planes.dat`.

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Đường bay có khai báo loại máy bay | 67.645 |
| Đường bay không khai báo loại máy bay | 18 |
| Cặp đường bay–mã loại máy bay sau khi tách | 93.231 |
| Mã loại máy bay khác nhau | 168 |
| Số mã nhiều nhất trên một bản ghi | 9 |

| Mã Equipment | Số bản ghi sau khi tách |
| --- | ---: |
| 320 | 15.514 |
| 738 | 10.406 |
| 319 | 7.885 |
| 321 | 3.677 |
| 73H | 3.351 |
| 737 | 2.787 |
| 73W | 2.502 |
| CRJ | 2.224 |
| E90 | 1.970 |
| AT7 | 1.635 |
| 73G | 1.592 |
| 333 | 1.589 |

18 bản ghi Equipment rỗng không tạo phần tử khi `split()` và `flatMap()`, nhưng vẫn nằm trong RDD routes gốc. Vì một đường bay có thể ghi nhiều loại máy bay, tổng 93.231 cặp lớn hơn số đường bay.

## Bài 5. Số đường bay theo quốc gia

**Mục tiêu:** đếm đường bay theo quốc gia/vùng lãnh thổ của sân bay xuất phát.

**Phương pháp:** chia routes thành nhóm tra được và không tra được mã sân bay đi bằng bảng broadcast. Với nhóm tra được, dùng `map()`, `reduceByKey(add)` tổng hợp theo giá trị Country trong `airports.dat`.

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Giá trị quốc gia/vùng lãnh thổ được thống kê | 225 |
| Đường bay tra được sân bay đi | 67.257 |
| Đường bay không tra được sân bay đi | 406 |
| Mã sân bay đi phân biệt không tra được | 157 |

| Quốc gia | Đường bay đi |
| --- | ---: |
| United States | 13.100 |
| China | 8.160 |
| United Kingdom | 2.663 |
| Spain | 2.531 |
| Germany | 2.352 |
| France | 1.930 |
| Canada | 1.852 |
| Russia | 1.843 |
| Italy | 1.776 |
| India | 1.507 |
| Brazil | 1.398 |
| Japan | 1.286 |

Kiểm tra: **67.257 + 406 = 67.663**. Nhóm “không tra được” có nghĩa mã không có trong bảng IATA đã lọc, không phải khẳng định sân bay không tồn tại. Bài này không dùng `countries.dat` để chuẩn hóa tên quốc gia.

## Bài 6. Mạng bay Việt Nam

**Mục tiêu:** thống kê đường bay đi/đến Việt Nam, sân bay xuất phát và hãng bay liên quan.

**Phương pháp:** `filter()` theo Country bằng `Vietnam` trong bảng broadcast. Lọc tiếp điểm đến để tìm nội địa; đếm theo sân bay bằng mã nguồn `p[2]`, theo hãng bằng Airline ID `p[1]`, dùng `reduceByKey(add)` và `collect()`. Tên hãng được lấy từ bảng tra `airlines.dat`.

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Đường bay xuất phát từ Việt Nam | 288 |
| Đường bay đến Việt Nam | 288 |
| Đường bay nội địa trong nhóm xuất phát từ Việt Nam | 126 |
| Phần còn lại theo cách đếm của đề: 288 − 126 | 162 |
| Trong phần còn lại: quốc tế xác định được | 161 |
| Trong phần còn lại: chưa tra được quốc gia đến | 1 |
| Sân bay có đường bay đi | 20 |
| Nhóm Airline ID có đường bay đi | 45 |

### Phân biệt nhóm 162 đường bay

Notebook tạo `quoc_te_vn` bằng điều kiện `not la_san_bay_vn(p[4])`. Hàm này cũng trả về `False` khi điểm đến không có trong bảng tra, nên output `Chuyen bay quoc te di: 162` gồm cả trường hợp chưa xác định được quốc gia đến.

Báo cáo làm rõ trường hợp đó là **SGN → THD**. Bản ghi kiểm tra trực tiếp trong dữ liệu:

```text
VN,5309,SGN,3205,THD,9135,,0,321
```

Vì vậy, cách diễn đạt kết quả là **126 nội địa + 161 quốc tế xác định được + 1 chưa phân loại = 288**. Không mô tả toàn bộ 162 bản ghi là quốc tế đã xác minh.

### Sân bay có đường bay xuất phát

Tên thành phố giữ theo output notebook.

| IATA | Đường bay đi | Thành phố |
| --- | ---: | --- |
| SGN | 109 | Ho Chi Minh City |
| HAN | 87 | Hanoi |
| DAD | 33 | Danang |
| BMV | 7 | Buonmethuot |
| CXR | 7 | Nha Trang |
| VII | 7 | Vinh |
| DLI | 5 | Dalat |
| PQC | 5 | Phuquoc |
| HPH | 4 | Haiphong |
| HUI | 4 | Hue |
| PXU | 3 | Pleiku |
| UIH | 3 | Phucat |
| VCA | 3 | Can Tho |
| TBB | 2 | Tuy Hoa |
| VCL | 2 | Chu Lai |
| VCS | 2 | Conson |
| VDH | 2 | Dong Hoi |
| CAH | 1 | Ca Mau |
| DIN | 1 | Dienbienphu |
| VKG | 1 | Rach Gia |

### Ba nhóm hãng có nhiều đường bay nhất

| Mã IATA tra được | Tên trong output/bảng airlines | Đường bay đi |
| --- | --- | ---: |
| VN | Vietnam Airlines | 139 |
| VJ | Royal Air Cambodge | 32 |
| BL | Jetstar Pacific | 18 |

Tên `Royal Air Cambodge` ứng với VJ được giữ nguyên từ bảng dữ liệu và output; tài liệu không tự thay bằng tên hãng hiện tại. Danh sách đầy đủ 45 nhóm hãng có trong cell thứ hai của Bài 6 và báo cáo.

Hai tổng đi và đến cùng bằng 288 không chứng minh từng đường bay có một tuyến ngược lại tương ứng, cũng không cho biết số chuyến bay thực tế ở mỗi chiều.

## Bài 7. Nội địa so với quốc tế trên toàn thế giới

**Mục tiêu:** phân loại mọi bản ghi theo quốc gia của sân bay đi và đến.

**Phương pháp:** hàm `phan_loai()` trả về “không tra được” nếu thiếu một trong hai sân bay; nếu tra được cả hai thì so sánh Country để phân biệt nội địa/quốc tế. Dùng `map()`, `reduceByKey(add)`, `collectAsMap()` tổng hợp ba nhóm.

| Nhóm | Số đường bay |
| --- | ---: |
| Nội địa | 32.167 |
| Quốc tế | 34.767 |
| Không tra được | 729 |
| Tổng | 67.663 |

Tỉ lệ quốc tế trên nhóm xác định được cả hai đầu:

```text
34.767 / (32.167 + 34.767) × 100 ≈ 51,9%
```

729 bản ghi không tra được không nằm trong mẫu số. Số này lớn hơn 406 ở Bài 5 vì Bài 5 chỉ cần tra điểm đi, còn Bài 7 cần tra cả điểm đi và điểm đến.

Xem [hướng dẫn chạy](Huong_dan_Lab2_BTVN.md) để tái hiện và lưu notebook có output.
