# Shop Mô Hình Siêu Nhân

Web bán mô hình siêu nhân, viết bằng **Django (Python)**. Gồm 2 phần:
- **Trang khách hàng**: xem danh sách mô hình, lọc theo hãng/giá, xem chi tiết, gửi yêu cầu đặt hàng.
- **Trang admin**: quản lý hãng, sản phẩm, yêu cầu đặt hàng, và doanh thu (nhập tay).

## 1. Cài đặt lần đầu

Cần có **Python 3.10+** cài sẵn trên máy.

```bash
# 1. Giải nén project, mở terminal tại thư mục gốc (chứa file manage.py)

# 2. Tạo môi trường ảo (venv)
python3 -m venv venv

# 3. Kích hoạt venv
# Trên macOS/Linux:
source venv/bin/activate
# Trên Windows:
venv\Scripts\activate

# 4. Cài các thư viện cần thiết
pip install -r requirements.txt

# 5. Tạo database (SQLite, tự động tạo file db.sqlite3)
python manage.py migrate

# 6. Tạo tài khoản admin (nhập username/password theo ý bạn)
python manage.py createsuperuser
```

## 2. Chạy thử project

```bash
python manage.py runserver
```

Sau đó mở trình duyệt:
- Trang khách hàng: http://127.0.0.1:8000/
- Trang admin: http://127.0.0.1:8000/admin/ (đăng nhập bằng tài khoản vừa tạo ở bước 6)

## 3. Cách dùng trang Admin

1. **Hãng**: vào mục "Hãng" trong admin, thêm hãng mới (VD: Bandai - Nhật Bản, YM Studio - Hàn Quốc).
2. **Mô hình**: vào mục "Mô hình", thêm sản phẩm mới — nhớ chọn Hãng, nhập giá, upload ảnh.
3. **Yêu cầu đặt hàng**: khi khách gửi form trên web, yêu cầu sẽ xuất hiện ở đây. Đánh dấu trạng thái "Đã liên hệ" sau khi gọi điện xác nhận, hoặc "Spam" nếu là yêu cầu rác.
4. **Doanh thu**: sau khi chốt đơn thành công, vào mục "Doanh thu" tự nhập: ngày bán, sản phẩm, giá bán thực tế. Hệ thống hiển thị tổng doanh thu theo bộ lọc ở đầu trang danh sách.

## 4. Cấu trúc project

```
shopconfig/       - Cấu hình chính của Django (settings, urls)
shop/              - App chính chứa toàn bộ logic
  models.py        - Định nghĩa dữ liệu: Brand, Product, OrderRequest, Revenue
  admin.py         - Cấu hình trang admin
  views.py         - Xử lý logic hiển thị trang, lọc sản phẩm, nhận form đặt hàng
  forms.py         - Form đặt hàng (có honeypot chống spam)
  urls.py          - Đường dẫn (route) của app
  templates/shop/  - Giao diện HTML
static/css/        - File CSS giao diện
media/             - Ảnh sản phẩm do admin upload (tự tạo khi chạy)
```

## 5. Chống spam trong form đặt hàng

- **Honeypot field**: 1 ô ẩn trong form, người dùng thật không thấy nên không điền. Bot tự động điền hết các ô kể cả ô ẩn → nếu ô này có giá trị, hệ thống âm thầm không lưu (không báo lỗi để tránh "dạy" bot).
- **Giới hạn tần suất**: mỗi địa chỉ IP chỉ được gửi tối đa **5 yêu cầu / giờ**. Nếu vượt quá sẽ hiện thông báo yêu cầu thử lại sau.

## 6. Khi cần deploy lên hosting thật (để khách truy cập được)

Project hiện chạy ở chế độ development (`DEBUG = True`), phù hợp để chạy thử trên máy cá nhân. Khi Nam sẵn sàng đưa web lên mạng cho khách xem, mình sẽ hỗ trợ thêm bước:
- Đổi `DEBUG = False`, cấu hình `ALLOWED_HOSTS`
- Đổi rate-limit cache sang Redis (nếu deploy nhiều tiến trình)
- Chọn nơi deploy phù hợp (VD: Railway, Render, VPS...) và tên miền

## 7. Cần chỉnh sửa gì thêm?

Cứ nhắn cho mình biết muốn thêm/sửa chức năng gì, mình sẽ hỗ trợ tiếp nhé.
