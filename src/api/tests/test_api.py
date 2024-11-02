from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from shop.utils.samples import sample_product, sample_related_product


# Create your tests here.
class TestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.product = sample_product("Test product")
        self.related_product = sample_related_product()

        self.user = get_user_model().objects.create(email="test@example.com")
        self.user.set_password("test1234")
        self.user.save()

        self.superuser = get_user_model().objects.create(email="test_super@example.com", is_superuser=True)
        self.superuser.set_password("test1234")
        self.superuser.save()

    def test_product_details(self):
        response = self.client.get(reverse("api:product-detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Test product",
                "price": "10.00",
                "is_sale": False,
                "sale_price": None,
                "status": "Active",
                "images": [],
                "category": {"id": 1, "name": "Test category"},
                "description": "Test description",
                "attributes": {},
            },
        )

    def test_product_related_products(self):
        response = self.client.get(
            reverse("api:product-related-products", kwargs={"pk": self.related_product.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "id": 3,
                    "name": "Test product #2",
                    "price": "10.00",
                    "is_sale": False,
                    "sale_price": None,
                    "status": "Active",
                    "images": [],
                }
            ],
        )

    def test_category_list(self):
        response = self.client.get(reverse("api:category-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": 1, "name": "Test category", "parent": None}])

    def test_create_product_without_permissions(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("api:product-create"), {"name": "Test product", "price": 10, "status": "Active", "category": 1}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data,
            {
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.", code="permission_denied"
                ),
            },
        )

    def test_create_product_with_permissions(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            reverse("api:product-create"), {"name": "Test product", "price": 10, "status": "Active", "category": 1}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": 4,
                "name": "Test product",
                "price": "10.00",
                "is_sale": False,
                "sale_price": None,
                "status": "Active",
                "category": 1,
                "description": "",
                "attributes": {},
            },
        )
