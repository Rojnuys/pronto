from rest_framework import status, viewsets
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsSuperUser
from api.serializers import (CategorySerializer, CommentSerializer,
                             CreateProductSerializer, FullProductSerializer,
                             ProductCommentSerializer, ProductImageSerializer,
                             ProductWithImagesSerializer,
                             RelatedProductSerializer)
from shop.models import (Category, Comment, Product, ProductImage,
                         RelatedProduct, Status)


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]


class CategoryProductListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductWithImagesSerializer

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs["pk"])


class ProductImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class RelatedProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = RelatedProduct.objects.all()
    serializer_class = RelatedProductSerializer


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductWithImagesSerializer


class ProductDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = FullProductSerializer


class ProductCreateView(CreateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for v, l in Status.choices:
            if l == serializer.validated_data["get_status_display"]:
                serializer.validated_data.pop("get_status_display")
                serializer.validated_data["status"] = v
                break
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsSuperUser]
    http_method_names = ["put", "patch"]
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if "get_status_display" in serializer.validated_data:
            for v, l in Status.choices:
                if l == serializer.validated_data["get_status_display"]:
                    serializer.validated_data.pop("get_status_display")
                    serializer.validated_data["status"] = v
                    break

            if "get_status_display" in serializer.validated_data:
                return Response({"status": "Incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)


class ProductDeleteView(RetrieveDestroyAPIView):
    permission_classes = [IsSuperUser]
    http_method_names = ["delete"]
    queryset = Product.objects.all()


class ProductCommentListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductCommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(product_id=self.kwargs["pk"], is_allowed=True)


class ProductRelatedProductListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductWithImagesSerializer

    def get_queryset(self):
        product = Product.objects.get(pk=self.kwargs["pk"])
        related_products = product.related_products.values_list("related_product", flat=True)
        return Product.objects.filter(pk__in=related_products)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
