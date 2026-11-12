# Xuất bản issue sau khi được duyệt

Rà 29 bản nháp theo ID, dependency, milestone và label. Xác nhận đúng remote mới, tài khoản, quyền và danh sách được duyệt trước khi dùng GitHub CLI. Kiểm issue đã có theo stable ID để tránh tạo trùng.

Ví dụ sau khi thay OWNER/REPO bằng đích đã duyệt, kiểm từng task rồi dùng `gh issue create --repo OWNER/REPO --title "[T01] Kiểm kê và bảo toàn repo cũ" --body-file issues/T01.md`. Gắn labels/milestone thật khi chúng tồn tại và lưu mapping Txx ↔ issue sau xuất bản.
