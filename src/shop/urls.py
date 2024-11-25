from django.urls import path

from shop.views import (CartAddRedirectView, CartChangeAmountRedirectView,
                        CartRemoveRedirectView, CartTemplateView,
                        CategoryProductsListView, ProductDetailView,
                        ProductListView, generate_categories,
                        generate_comments, generate_products, OrderCreateView, OrderListView, OrderDetailView,
                        CommentListView, ProductSearchListView, generate_slider_items)

app_name = "shop"

urlpatterns = [
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/comments", CommentListView.as_view(), name="product_comments"),
    path("products/search", ProductSearchListView.as_view(), name="product_search"),
    path("categories/<int:pk>", CategoryProductsListView.as_view(), name="category_products_list"),
    path("cart", CartTemplateView.as_view(), name="cart"),
    path("cart/add", CartAddRedirectView.as_view(), name="cart_add"),
    path("cart/change", CartChangeAmountRedirectView.as_view(), name="cart_change"),
    path("cart/remove", CartRemoveRedirectView.as_view(), name="cart_remove"),
    path("order/create", OrderCreateView.as_view(), name="order_create"),
    path("orders", OrderListView.as_view(), name="order_list"),
    path("order/<int:pk>", OrderDetailView.as_view(), name="order_detail"),
    path("generate/categories", generate_categories, name="generate_categories"),
    path("generate/categories/<int:count>", generate_categories, name="generate_categories"),
    path("generate/products", generate_products, name="generate_products"),
    path("generate/products/<int:count>", generate_products, name="generate_products"),
    path("generate/comments", generate_comments, name="generate_comments"),
    path("generate/comments/<int:count>", generate_comments, name="generate_comments"),
    path("generate/slider-items", generate_slider_items, name="generate_slider_items"),
    path("generate/slider-items/<int:count>", generate_slider_items, name="generate_slider_items"),
]
