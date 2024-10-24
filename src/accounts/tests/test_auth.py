from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


# Create your tests here.
class TestAuth(TestCase):
    def setUp(self):
        self.client = Client()

        self.customer = get_user_model().objects.create(email="customer@customer.com")
        self.customer_password = "customer"
        self.customer.set_password(self.customer_password)
        self.customer.save()

        self.manager = get_user_model().objects.create(email="manager@manager.com", is_staff=True)
        self.manager.set_password("manager")
        self.manager.save()

    def test_auth_with_incorrect_email(self):
        is_login = self.client.login(email="incorrect email", password=self.customer_password)
        self.assertFalse(is_login)

    def test_auth_with_incorrect_password(self):
        is_login = self.client.login(email=self.customer.email, password="incorrect password")
        self.assertFalse(is_login)

    def test_auth_successfully(self):
        is_login = self.client.login(email=self.customer.email, password=self.customer_password)
        self.assertTrue(is_login)

    def test_customer_access_admin_panel(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_manager_access_admin_panel(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
