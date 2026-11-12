# Giao thức thực nghiệm dự kiến

Trục 1 kiểm DApriori và Parallel FP-Growth trên cùng basket, ngưỡng và phạm vi so kết quả k≤2. Ghi phạm vi hai implementation thực sự xử lý khi so thời gian. Trục 2 chỉ so Java Hadoop MapReduce với Spark trên tác vụ đếm cặp, cùng file input, quy tắc dedup, schema và tài nguyên được mô tả. So toàn bộ output trước khi đo.

Chọn tập theo order_id và seed, giữ basket trọn. Ghi input URI/scope, hash/manifest, N, commit, runtime, CPU/RAM, parallelism/partitions/reducers, cache policy, warmup, phiên bản và lệnh. Tách preprocessing, fit/đếm, sinh luật, export nếu có. Lặp ít nhất ba lần ở các cấu hình khả thi; lưu mọi lần chạy, lỗi, độ biến thiên và phạm vi đo bộ nhớ nếu có.

Mô tả rõ Spark local, Hadoop pseudo-distributed hay cluster nhiều node. Ghi giới hạn máy và khác biệt workload khi diễn giải. Kết quả đo mới nằm trong T25–T26.
