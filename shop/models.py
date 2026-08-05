from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^0\d{9}$',
    message="Số điện thoại phải gồm 10 chữ số và bắt đầu bằng số 0 (VD: 0912345678)."
)


class Brand(models.Model):
    """Hãng sản xuất mô hình, ví dụ: Bandai (Nhật), Sentinel (Nhật), YM Studio (Hàn)..."""
    name = models.CharField("Tên dòng", max_length=100)
    country = models.CharField(
        "Quốc gia",
        max_length=20,
        choices=[("JP", "Nhật Bản"), ("KR", "Hàn Quốc"), ("US", "Mỹ"), ("HK", "HongKong")],
        default="JP",
    )

    class Meta:
        verbose_name = "Hãng"
        verbose_name_plural = "Hãng"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_country_display()})"


class Product(models.Model):
    """Mô hình siêu nhân."""
    name = models.CharField("Tên mô hình", max_length=200)
    brand = models.ForeignKey(Brand, verbose_name="Hãng", on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField("Giá (VNĐ)", max_digits=12, decimal_places=0)
    description = models.TextField("Mô tả", blank=True)
    image = models.ImageField("Ảnh đại diện", upload_to="products/", blank=True, null=True)
    video = models.FileField("Video ngắn (giới thiệu, 20-30s)", upload_to="products/videos/", blank=True, null=True)
    is_active = models.BooleanField("Đang bán", default=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

    class Meta:
        verbose_name = "Mô hình"
        verbose_name_plural = "Mô hình"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    """Ảnh bổ sung cho sản phẩm (ngoài ảnh đại diện chính)."""
    product = models.ForeignKey(Product, verbose_name="Mô hình", on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField("Ảnh", upload_to="products/gallery/")
    order = models.PositiveIntegerField("Thứ tự", default=0)

    class Meta:
        verbose_name = "Ảnh sản phẩm"
        verbose_name_plural = "Ảnh sản phẩm"
        ordering = ["order", "id"]

    def __str__(self):
        return f"Ảnh của {self.product.name}"

class OrderRequest(models.Model):
    """Yêu cầu đặt hàng gửi từ khách, admin xử lý và lên đơn thủ công."""

    STATUS_CHOICES = [
        ("new", "Mới"),
        ("contacted", "Đã liên hệ"),
        ("spam", "Spam - Đã ẩn"),
    ]

    customer_name = models.CharField("Tên khách hàng", max_length=100)
    phone = models.CharField("Số điện thoại", max_length=15, validators=[phone_validator])
    address = models.CharField("Địa chỉ", max_length=255)
    product = models.ForeignKey(Product, verbose_name="Mô hình muốn mua", on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField("Ghi chú", blank=True)
    status = models.CharField("Trạng thái", max_length=10, choices=STATUS_CHOICES, default="new")
    ip_address = models.GenericIPAddressField("Địa chỉ IP", null=True, blank=True)
    created_at = models.DateTimeField("Ngày gửi", auto_now_add=True)

    class Meta:
        verbose_name = "Yêu cầu đặt hàng"
        verbose_name_plural = "Yêu cầu đặt hàng"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.product} ({self.get_status_display()})"


class Revenue(models.Model):
    """Doanh thu, admin nhập tay sau khi chốt đơn."""
    date = models.DateField("Ngày bán")
    product = models.ForeignKey(Product, verbose_name="Mô hình đã bán", on_delete=models.SET_NULL, null=True, blank=True)
    sale_price = models.DecimalField("Giá bán thực tế (VNĐ)", max_digits=12, decimal_places=0)
    note = models.CharField("Ghi chú", max_length=255, blank=True)
    created_at = models.DateTimeField("Ngày nhập", auto_now_add=True)

    class Meta:
        verbose_name = "Doanh thu"
        verbose_name_plural = "Doanh thu"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} - {self.product} - {self.sale_price:,.0f}đ"
