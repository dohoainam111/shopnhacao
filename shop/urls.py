from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("san-pham/<int:pk>/", views.product_detail, name="product_detail"),
    path("dat-hang/", views.order_request_create, name="order_request_create"),
    path("dat-hang/<int:pk>/", views.order_request_create, name="order_request_create_for_product"),
]
