from django.core.exceptions import ValidationError
from django.test import TestCase

from shop.utils.samples import sample_product, sample_related_product


# Create your tests here.
class TestProduct(TestCase):
    def setUp(self):
        self.product = sample_product("Test product #1")

    def test_saving_product_on_sale_without_sale_price(self):
        self.product.is_sale = True
        self.assertRaises(ValidationError, self.product.save)

    def test_saving_product_on_sale_with_sale_price(self):
        self.product.is_sale = True
        self.product.sale_price = 100
        self.assertIsNone(self.product.save())

    def test_get_price_if_product_on_sale(self):
        self.product.is_sale = True
        self.product.price = 200
        self.product.sale_price = 100
        self.assertEqual(self.product.get_price(), 100)

    def test_get_price_if_product_no_sale(self):
        self.product.price = 200
        self.product.sale_price = 100
        self.assertEqual(self.product.get_price(), 200)


class TestRelatedProduct(TestCase):
    def setUp(self):
        self.related_product = sample_related_product()

    def test_saving_related_product_is_not_the_same(self):
        self.assertIsNone(self.related_product.save())

    def test_saving_related_product_is_the_same(self):
        product = sample_product("Test product #1")
        self.related_product.product = product
        self.related_product.related_product = product
        self.assertRaises(ValidationError, self.related_product.save)
