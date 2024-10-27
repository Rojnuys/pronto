from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryProductListView, CategoryViewSet,
                       CommentViewSet, ProductCommentListView,
                       ProductCreateView, ProductDeleteView, ProductDetailView,
                       ProductImageViewSet, ProductListView,
                       ProductRelatedProductListView, ProductUpdateView,
                       RelatedProductViewSet)

app_name = "api"

category_router = routers.DefaultRouter()
category_router.register("categories", CategoryViewSet)

comment_router = routers.DefaultRouter()
comment_router.register("comments", CommentViewSet)

product_image_router = routers.DefaultRouter()
product_image_router.register("product-images", ProductImageViewSet)

related_product_router = routers.DefaultRouter()
related_product_router.register("related-products", RelatedProductViewSet)

urlpatterns = [
    path("", include(category_router.urls)),
    path("", include(product_image_router.urls)),
    path("", include(related_product_router.urls)),
    path("", include(comment_router.urls)),
    path("categories/<int:pk>/products/", CategoryProductListView.as_view(), name="category_products"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path(
        "products/<int:pk>/related-products/", ProductRelatedProductListView.as_view(), name="product_related_products"
    ),
    path("products/<int:pk>/comments/", ProductCommentListView.as_view(), name="product_comments"),
]
