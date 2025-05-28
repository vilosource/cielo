from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import AzureSubscription # Import the new model

def get_navigation_items(request):
    """
    Returns a list of navigation items for the inventory app,
    respecting the current user's permissions.
    """
    items = []

    # Note: 'inventory.view_virtualmachine' and 'inventory.view_storageaccount'
    # are placeholder permission codenames. These would typically be generated
    # by Django if you have VirtualMachine and StorageAccount models in this app.
    # For now, only superusers will see these links by default, or users
    # explicitly granted these (currently non-existent) permissions.

    if request.user.has_perm('inventory.view_virtualmachine'):
        items.append({
            'label': _('Virtual Machines'),
            'url': reverse('inventory:virtual_machines'),
            'icon_class': 'bi-hdd-stack', # Bootstrap icon class
            'active_pattern_names': ['inventory:virtual_machines'], # For highlighting active link
        })

    if request.user.has_perm('inventory.view_storageaccount'):
        items.append({
            'label': _('Storage Accounts'),
            'url': reverse('inventory:storage_accounts'),
            'icon_class': 'bi-database-fill-gear', # Bootstrap icon class
            'active_pattern_names': ['inventory:storage_accounts'],
        })

    # Subscriptions Menu
    if request.user.has_perm('inventory.view_azuresubscription'):
        subscription_sub_items = []
        try:
            # Fetch subscriptions from the database
            # In a real app with many subscriptions, consider caching or optimizing this query.
            subscriptions = AzureSubscription.objects.all()
            for sub in subscriptions:
                subscription_sub_items.append({
                    'label': sub.name,
                    'url': reverse('inventory:azure_subscription_detail', kwargs={'pk': sub.pk}),
                    'icon_class': 'bi-cloud', # Example icon for individual subscriptions
                    'active_pattern_names': ['inventory:azure_subscription_detail'], # Add specific active check if needed
                })
        except Exception: # Catch potential database errors during startup if migrations haven't run
            pass

        if subscription_sub_items: # Only add the parent menu if there are subscriptions to show
            items.append({
                'label': _('Azure Subscriptions'),
                'icon_class': 'bi-clouds-fill', # Icon for the parent menu
                'sub_items': subscription_sub_items,
                # 'url': reverse('inventory:azure_subscriptions_list'), # Optional: if you want a page listing all subscriptions
            })
    return items

def get_app_permissions():
    """
    Returns a list of permissions this app defines or relies on.
    """
    return [
        ('view_virtualmachine', _('Can view virtual machines')),
        ('view_storageaccount', _('Can view storage accounts')),
        ('view_azuresubscription', _('Can view Azure subscriptions')),
        # Add other permissions as your app defines them, e.g., add_virtualmachine, etc.
    ]