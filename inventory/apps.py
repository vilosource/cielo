from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
    verbose_name = _("Infrastructure Inventory")

    # CIELO Core Integration Hooks
    cielo_app_label = _("Inventory")
    cielo_icon_class = "bi-archive"  # Example Bootstrap Icon

    # Path to a function that provides navigation items for this app
    cielo_navigation_provider = "inventory.cielo_hooks.get_navigation_items"

    # Path to a function that provides permission definitions for this app
    cielo_permissions_provider = "inventory.cielo_hooks.get_app_permissions"
