from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django_ratelimit.decorators import ratelimit
from .models import Product, Brand
from .forms import OrderRequestForm


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related("brand")

    brand_id = request.GET.get("brand")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if brand_id:
        products = products.filter(brand_id=brand_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "brands": Brand.objects.all(),
        "selected_brand": brand_id or "",
        "min_price": min_price or "",
        "max_price": max_price or "",
    }
    return render(request, "shop/product_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, "shop/product_detail.html", {"product": product})


@ratelimit(key="ip", rate="5/h", method="POST", block=False)
def order_request_create(request, pk=None):
    was_limited = getattr(request, "limited", False)
    if not pk:
        return redirect("shop:product_list")

    was_limited = getattr(request, "limited", False)
    product = get_object_or_404(Product, pk=pk, is_active=True)

    if request.method == "POST":
        if was_limited:
            messages.error(request, "Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 giờ.")
            return redirect("shop:product_list")

        form = OrderRequestForm(request.POST)
        if form.is_valid():
            if form.is_honeypot_triggered():
                # Giả vờ thành công để không "dạy" cho bot biết bị chặn, nhưng không lưu gì cả.
                messages.success(request, "Gửi yêu cầu thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.")
                return redirect("shop:product_list")

            order = form.save(commit=False)
            order.product = product
            order.ip_address = get_client_ip(request)
            order.save()
            messages.success(request, "Gửi yêu cầu thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.")
            return redirect("shop:product_list")
    else:
        initial = {"product": product} if product else {}
        form = OrderRequestForm(initial=initial)

    return render(request, "shop/order_request_form.html", {"form": form, "product": product})
