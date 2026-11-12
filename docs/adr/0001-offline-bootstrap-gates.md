# ADR 0001 — Cổng kiểm tra chạy offline

Trạng thái Proposed, chờ review bootstrap.

Nhóm có hai thành viên và chưa chốt remote hoặc quyền GitHub. Registry TOML là nguồn phạm vi và dependency của task. Review thật có bằng chứng để mở downstream; PR kiểm lại contract và artifact của dependency trên base. CI fixture chạy độc lập với dịch vụ HDFS, dữ liệu lớn và tài khoản GitHub Project.

Hệ quả là task metadata và issue drafts có thể rà từ checkout cục bộ. Khi có remote và quyền, nhóm quyết định cách đồng bộ issues và branch protection mà không thay đổi contract CLI.

Đặc tả khởi tạo được lưu cục bộ theo chỉ dẫn của chủ dự án. Git dùng `.git/info/exclude` cho các tệp prompt. Bản clone dùng `docs/requirements.md` làm đầu vào chung. Hook Git và CI kiểm tra quy tắc lưu prompt cục bộ.
