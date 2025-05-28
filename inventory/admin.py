from django.contrib import admin
from .models import VirtualMachine, StorageAccount, AzureSubscription

admin.site.register(VirtualMachine)
admin.site.register(StorageAccount)
admin.site.register(AzureSubscription)