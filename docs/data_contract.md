# Contract dữ liệu dự kiến

T09 xác minh metadata, schema nguồn, nullable, tên file và hash công bố nếu có. T10 lưu manifest với source URL, tên tệp, byte, checksum cục bộ, split, thời điểm tiếp nhận và URI lưu trữ. Prior/full thật là đầu vào đánh giá. Train và fixture được ghi rõ scope. Giữ raw ngoài Git.

## Basket và đầu ra

- Một basket mỗi `order_id`. Dùng `product_id` hợp lệ, duy nhất và sắp xếp tăng dần. `user_id` là thuộc tính của order.
- Join và audit theo khóa. Ghi duplicate, invalid, orphan, null hợp lệ và số hàng/basket trước/sau từng thao tác.
- Itemset có `items` chuẩn hóa, `freq` nguyên, `support = freq/N`. Dùng ngưỡng đếm bao gồm biên `ceil(s*N)`.
- Luật A→B có `support = count(A∪B)/N`, `confidence = count(A∪B)/count(A)`, `lift = confidence/support(B)`. Không tính khi mẫu số bằng 0.
- Hai job đếm cặp dùng cùng schema `product_a,product_b,count`, A<B và mỗi basket đóng góp tối đa một lần cho một pair.

Fixture bootstrap `tests/fixtures/baskets.csv` chỉ kiểm gates. Fixture Instacart nhiều bảng và bản ghi xấu sẽ do T09 tạo.
