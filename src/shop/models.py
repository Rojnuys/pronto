from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseShopModel


# Create your models here.
class Category(BaseShopModel):
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Status(models.IntegerChoices):
    ACTIVE = 0, _("Active")
    INACTIVE = 1, _("Inactive")
    OUT_OF_STOCK = 2, _("Out of stock")


class Product(BaseShopModel):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=150)
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.01),
            validators.MaxValueValidator(99999999.99),
        ],
    )
    is_sale = models.BooleanField(_("is sale"), default=False)
    sale_price = models.DecimalField(
        _("sale price"),
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.01),
            validators.MaxValueValidator(99999999.99),
        ],
        null=True,
        blank=True,
    )
    status = models.PositiveSmallIntegerField(_("status"), choices=Status, default=Status.ACTIVE)
    description = models.TextField(_("description"), blank=True)
    attributes = models.JSONField(_("attributes"), default=dict, blank=True)

    def get_price(self):
        return self.sale_price if self.is_sale else self.price

    def clean(self):
        if self.is_sale and not self.sale_price:
            raise ValidationError("The product is on sale, so the sale price is required.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RelatedProduct(BaseShopModel):
    product = models.ForeignKey(Product, related_name="related_products", on_delete=models.CASCADE)
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = [("product", "related_product")]

    def clean(self):
        if self.product == self.related_product:
            raise ValidationError("Product and related product cannot be the same.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.related_product.name}"


class ProductImage(BaseShopModel):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        _("image"),
        upload_to="products",
        max_length=15 * 1024,
        validators=[validators.FileExtensionValidator(allowed_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)],
    )
    order_number = models.PositiveSmallIntegerField(
        _("order number"),
        default=1,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12),
        ],
    )

    class Meta:
        unique_together = [("product", "order_number")]
        ordering = ["order_number"]

    def __str__(self):
        return f"{self.product.name} - {self.order_number}"


class Rating(models.IntegerChoices):
    VERY_BAD = 1, _("Very bad")
    BAD = 2, _("Bad")
    NORMAL = 3, _("Normal")
    GOOD = 4, _("Good")
    EXCELLENT = 5, _("Excellent")


class Comment(BaseShopModel):
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField(_("content"), max_length=500, null=True, blank=True)
    advantages = models.CharField(_("advantages"), max_length=150, null=True, blank=True)
    disadvantages = models.CharField(_("disadvantages"), max_length=150, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        _("rating"),
        choices=Rating,
        default=Rating.EXCELLENT,
    )
    is_allowed = models.BooleanField(_("is allowed"), default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} - {self.rating}"


class OrderStatus(models.IntegerChoices):
    PROCESSING = 0, _("Processing")
    ON_THE_WAY = 1, _("On the way")
    DELIVERED = 2, _("Delivered")
    FINISHED_SUCCESSFULLY = 3, _("Finished successfully")
    FINISHED_UNSUCCESSFULLY = 4, _("Finished unsuccessfully")


class Order(BaseShopModel):
    user = models.ForeignKey(get_user_model(), related_name="orders", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderProduct")
    address = models.CharField(_("address"), max_length=255)
    status = models.PositiveSmallIntegerField(_("status"), choices=OrderStatus, default=OrderStatus.PROCESSING)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"


class OrderProduct(BaseShopModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price_at_purchase = models.DecimalField(_("price at purchase"), max_digits=10, decimal_places=2)

    class Meta:
        unique_together = [("order", "product")]

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in Order {self.order}"
