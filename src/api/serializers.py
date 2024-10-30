from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from shop.models import (Category, Comment, Product, ProductImage,
                         RelatedProduct)


class SimpleCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategorySerializer(SimpleCategorySerializer):
    class Meta:
        model = SimpleCategorySerializer.Meta.model
        fields = SimpleCategorySerializer.Meta.fields + ["parent"]


class SimpleProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "order_number"]


class ProductImageSerializer(SimpleProductImageSerializer):
    class Meta:
        model = SimpleProductImageSerializer.Meta.model
        fields = SimpleProductImageSerializer.Meta.fields + ["product"]


class SimpleProductSerializer(ModelSerializer):
    status = CharField(source="get_status_display")

    class Meta:
        model = Product
        fields = ["id", "name", "price", "is_sale", "sale_price", "status"]


class ProductWithImagesSerializer(SimpleProductSerializer):
    images = SimpleProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = SimpleProductSerializer.Meta.model
        fields = SimpleProductSerializer.Meta.fields + ["images"]


class FullProductSerializer(ProductWithImagesSerializer):
    category = SimpleCategorySerializer()

    class Meta:
        model = ProductWithImagesSerializer.Meta.model
        fields = ProductWithImagesSerializer.Meta.fields + ["category", "description", "attributes"]


class CreateProductSerializer(SimpleProductSerializer):
    class Meta:
        model = SimpleProductSerializer.Meta.model
        fields = SimpleProductSerializer.Meta.fields + ["category", "description", "attributes"]


class ProductCommentSerializer(ModelSerializer):
    rating = CharField(source="get_rating_display")

    class Meta:
        model = Comment
        fields = ["id", "content", "advantages", "disadvantages", "rating", "created_at"]


class RelatedProductSerializer(ModelSerializer):
    class Meta:
        model = RelatedProduct
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "product", "content", "advantages", "disadvantages", "rating", "created_at"]
