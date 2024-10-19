from django.core.exceptions import ValidationError
from django.test import TestCase

from shop.utils.samples import sample_product


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
