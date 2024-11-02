from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

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

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", include(category_router.urls)),
    path("", include(product_image_router.urls)),
    path("", include(related_product_router.urls)),
    path("", include(comment_router.urls)),
    path("categories/<int:pk>/products/", CategoryProductListView.as_view(), name="category-products"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
    path(
        "products/<int:pk>/related-products/", ProductRelatedProductListView.as_view(), name="product-related-products"
    ),
    path("products/<int:pk>/comments/", ProductCommentListView.as_view(), name="product-comments"),
]
