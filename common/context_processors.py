from django.conf import settings
from django.apps import apps
from django.utils.module_loading import import_string
import logging

logger = logging.getLogger(__name__)

def cielo_navigation_context(request):
    """
    Aggregates navigation items from all installed CIELO apps
    that provide a 'cielo_navigation_provider'.
    """
    navigation_items = []
    for app_name in settings.INSTALLED_APPS:
        try:
            app_config = apps.get_app_config(app_name)
            if hasattr(app_config, 'cielo_navigation_provider'):
                provider_path = app_config.cielo_navigation_provider
                navigation_provider_func = import_string(provider_path)
                app_nav_items = navigation_provider_func(request)
                if app_nav_items:
                    navigation_items.extend(app_nav_items)
        except LookupError:
            # Not a Django app, or app not found (e.g., django.contrib.admin not in apps.py)
            pass
        except Exception as e:
            logger.error(f"Error loading navigation from app {app_name} using provider {getattr(app_config, 'cielo_navigation_provider', 'N/A')}: {e}", exc_info=True)

    # You might want to sort navigation_items here if a specific order is desired across apps
    return {'cielo_navigation_items': navigation_items}