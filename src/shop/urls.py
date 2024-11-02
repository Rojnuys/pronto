from django.urls import path

from shop.views import ProductDetailView, ProductListView

app_name = "shop"

urlpatterns = [
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
]
