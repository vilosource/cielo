from django.db import models
from django.utils.translation import gettext_lazy as _

class VirtualMachine(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    environment = models.CharField(_("Environment"), max_length=50, blank=True)
    subscription = models.ForeignKey('AzureSubscription', on_delete=models.SET_NULL, related_name='virtual_machines', null=True, blank=True)
    # Add other relevant fields like OS, size, IP address, status, etc.

    class Meta:
        verbose_name = _("Virtual Machine")
        verbose_name_plural = _("Virtual Machines")
        # Django automatically creates view_virtualmachine, add_virtualmachine, etc.

    def __str__(self):
        return self.name

class StorageAccount(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    sku = models.CharField(_("SKU"), max_length=50, blank=True)
    access_tier = models.CharField(_("Access Tier"), max_length=50, blank=True)
    # Add other relevant fields like kind, replication, creation_date, etc.

    class Meta:
        verbose_name = _("Storage Account")
        verbose_name_plural = _("Storage Accounts")

    def __str__(self):
        return self.name

class AzureSubscription(models.Model):
    name = models.CharField(_("Subscription Name"), max_length=255)
    subscription_id = models.CharField(_("Azure Subscription ID"), max_length=36, unique=True, help_text="The unique GUID for the Azure Subscription.")
    # tenant_id = models.CharField(_("Azure Tenant ID"), max_length=36, blank=True, help_text="Optional: The AAD Tenant ID.")

    class Meta:
        verbose_name = _("Azure Subscription")
        verbose_name_plural = _("Azure Subscriptions")
        ordering = ['name']

    def __str__(self):
        return self.name