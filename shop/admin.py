from django.contrib import admin
from django.db.models import Sum
from .models import Brand, Product, OrderRequest, Revenue, ProductImage
from django import forms
from .forms import MultipleFileField , ImagePreviewWidget, VideoPreviewWidget
from django.utils.html import format_html
from django.db import models

admin.site.site_header = "Quản trị Shop nhà Cáo"      # chữ hiện ở đầu mọi trang admin
admin.site.site_title = "Shop Shop nhà Cáo"                 # chữ hiện trên tab trình duyệt
admin.site.index_title = "Trang quản trị Shop nhà Cáo"   
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)
    search_fields = ("name",)



class ProductAdminForm(forms.ModelForm):
    gallery_images = MultipleFileField(label="Thêm nhiều ảnh chi tiết (quét chọn cùng lúc)", required=False)
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "image": ImagePreviewWidget(),
            "video": VideoPreviewWidget(),
        }

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ("image", "order")
    formfield_overrides = {
        models.ImageField: {"widget": ImagePreviewWidget},
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "brand", "price", "is_sold", "is_active", "created_at")
    list_filter = ("brand", "is_active", "is_sold", "brand__country")
    search_fields = ("name",)
    list_editable = ("price", "is_active", "is_sold")
    inlines = [ProductImageInline]

    fields = (
        "name", "brand", "price", "description",
        "image",
        "video",
        "gallery_images",
        "is_sold", "is_active",
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        files = form.cleaned_data.get("gallery_images")
        if files:
            for f in files:
                ProductImage.objects.create(product=obj, image=f)


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "phone", "product", "status", "created_at", "ip_address")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone", "address")
    list_editable = ("status",)
    readonly_fields = ("ip_address", "created_at")
    actions = ["mark_contacted", "mark_spam"]
    list_per_page = 10

    @admin.action(description="Đánh dấu Đã liên hệ")
    def mark_contacted(self, request, queryset):
        queryset.update(status="contacted")

    @admin.action(description="Đánh dấu Spam")
    def mark_spam(self, request, queryset):
        queryset.update(status="spam")


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ("date", "product", "sale_price", "note")
    list_filter = ("date",)
    date_hierarchy = "date"
    list_per_page = 10

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data["cl"].queryset
            total = qs.aggregate(total=Sum("sale_price"))["total"] or 0
            response.context_data["summary_total"] = f"{total:,.0f}"
        except (AttributeError, KeyError):
            pass
        return response
