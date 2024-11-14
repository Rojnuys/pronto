from django.urls import path

from shop.views import (CartAddRedirectView, CartChangeAmountRedirectView,
                        CartRemoveRedirectView, CartTemplateView,
                        CategoryProductsListView, ProductDetailView,
                        ProductListView)

app_name = "shop"

urlpatterns = [
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("categories/<int:pk>", CategoryProductsListView.as_view(), name="category_products_list"),
    path("cart", CartTemplateView.as_view(), name="cart"),
    path("cart/add", CartAddRedirectView.as_view(), name="cart_add"),
    path("cart/change", CartChangeAmountRedirectView.as_view(), name="cart_change"),
    path("cart/remove", CartRemoveRedirectView.as_view(), name="cart_remove"),
]
