from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from shop.models import (Category, Comment, Order, OrderProduct, Product,
                         ProductImage, RelatedProduct)


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class RelatedProductInline(admin.TabularInline):
    model = RelatedProduct
    extra = 1
    fk_name = "product"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields["related_product"].queryset = formset.form.base_fields[
                "related_product"
            ].queryset.exclude(id=obj.id)
        return formset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price"]
    inlines = [ProductImageInline, RelatedProductInline]
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["created_at", "content", "rating"]


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["created_at", "updated_at", "status"]
    inlines = [OrderProductInline]
