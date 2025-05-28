from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventory.models import AzureSubscription, VirtualMachine


class ViewTests(TestCase):
    def setUp(self):
        self.password = "pass123"
        self.user = get_user_model().objects.create_user(
            username="testuser", password=self.password
        )
        self.subscription = AzureSubscription.objects.create(
            name="Sub1",
            subscription_id="12345678-1234-1234-1234-123456789012",
        )
        VirtualMachine.objects.create(name="vm1", subscription=self.subscription)

    def test_login_view_get(self):
        url = reverse("users:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_password_change_view_get(self):
        self.client.login(username="testuser", password=self.password)
        url = reverse("users:change_password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/change_password.html")

    def test_logout_view_get(self):
        self.client.login(username="testuser", password=self.password)
        url = reverse("users:logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/logout.html")

    def test_virtual_machines_view(self):
        self.client.login(username="testuser", password=self.password)
        url = reverse("inventory:virtual_machines")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/virtual_machines.html")

    def test_storage_accounts_view(self):
        self.client.login(username="testuser", password=self.password)
        url = reverse("inventory:storage_accounts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/storage_accounts.html")

    def test_azure_subscription_detail_view(self):
        self.client.login(username="testuser", password=self.password)
        url = reverse("inventory:azure_subscription_detail", args=[self.subscription.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/azure_subscription_detail.html")
