from django.core.exceptions import ValidationError
from django.test import TestCase

from shop.utils.samples import sample_product, sample_related_product


# Create your tests here.
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
