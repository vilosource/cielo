# Dynamic App Integration in CIELO

CIELO is designed with a modular architecture at its core, allowing for specialized functionalities to be developed as independent "CIELO Apps" that plug into the foundational "CIELO Core" platform. This document outlines how this dynamic integration is achieved, enabling apps to contribute UI elements (like navigation) and declare their capabilities (like permissions) to the Core.

## Core Concepts

1.  **CIELO Core:**
    *   Provides essential platform services: user authentication, authorization, session management, the overall UI shell (base templates, navigation bars, sidebars), and mechanisms for app discovery.
    *   Is responsible for discovering and integrating "CIELO Apps."
    *   Renders common UI elements, incorporating content and navigation provided by active and authorized apps.

2.  **CIELO Apps:**
    *   Are self-contained Django applications.
    *   Focus on specific functionalities (e.g., Azure VM management, AWS S3 bucket management, the example `inventory` app).
    *   Define their own models, views, templates, URLs, and business logic.
    *   **Crucially, they declare their integration points with the CIELO Core.**

## Integration Mechanism: `AppConfig` and `cielo_hooks.py`

The primary mechanism for a CIELO App to communicate its capabilities to the CIELO Core is through its Django `AppConfig` (typically found in `app_name/apps.py`) and a dedicated hooks module (conventionally `app_name/cielo_hooks.py`).

### 1. App Configuration (`apps.py`)

Each CIELO App uses its `AppConfig` to declare metadata and pointers to its integration hook functions.

**Example: `inventory/apps.py` (after refactoring for dynamic integration)**
```python
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
    verbose_name = _("Infrastructure Inventory")

    # CIELO Core Integration Hooks
    cielo_app_label = _("Inventory")  # Short, display name for the app
    cielo_icon_class = "bi-archive"  # Bootstrap Icon class for menus

    # Path to a function that provides navigation items for this app
    cielo_navigation_provider = "inventory.cielo_hooks.get_navigation_items"

    # Path to a function that provides permission definitions for this app
    cielo_permissions_provider = "inventory.cielo_hooks.get_app_permissions"

    # Optional: Path to the app's primary entry URL name (for a main app link)
    # cielo_entry_point_url_name = "inventory:dashboard"
```

### 2. Hook Implementations (`cielo_hooks.py`)

This module within each app contains the actual functions that the Core will call.

**Example: `inventory/cielo_hooks.py`**
```python
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

def get_navigation_items(request):
    """
    Returns a list of navigation items for this app,
    respecting the current user's permissions.
    """
    items = []
    # Example for Virtual Machines link
    if request.user.has_perm('inventory.view_virtualmachine'): # Assumes standard Django permission
        items.append({
            'label': _('Virtual Machines'),
            'url': reverse('inventory:virtual_machines'), # URL name from app's urls.py
            'icon_class': 'bi-hdd-stack', # App-specific icon
            'active_pattern_names': ['inventory:virtual_machines'], # For UI active state
        })
    # Example for Storage Accounts link
    if request.user.has_perm('inventory.view_storageaccount'):
        items.append({
            'label': _('Storage Accounts'),
            'url': reverse('inventory:storage_accounts'),
            'icon_class': 'bi-database-fill-gear',
            'active_pattern_names': ['inventory:storage_accounts'],
        })
    # Apps can return more complex structures, e.g., for sub-menus
    return items

def get_app_permissions():
    """
    Returns a list of permissions this app defines or relies on.
    Format: list of tuples: (codename, description)
    These should align with permissions defined in the app's models' Meta.permissions
    or custom permissions created programmatically.
    """
    return [
        ('view_virtualmachine', _('Can view virtual machines')),
        ('add_virtualmachine', _('Can add virtual machines')),
        ('view_storageaccount', _('Can view storage accounts')),
        # ... other permissions
    ]
```

## CIELO Core's Role

The CIELO Core will:
1.  **Discover Apps:** On startup, iterate through `settings.INSTALLED_APPS`, inspect each app's `AppConfig` for `cielo_*` attributes, and register the provided hook functions.
2.  **Render UI:** At request time (e.g., via context processors or template tags), call the registered `cielo_navigation_provider` functions from all integrated apps, passing the current `request`. It then aggregates these items to dynamically build the main navigation menus (e.g., the sidebar).
3.  **Manage Permissions (Future):** The data from `cielo_permissions_provider` can be used by the Core to build a centralized UI for administrators to view and manage permissions across all installed CIELO Apps.

## Benefits

*   **Decoupling:** Core and Apps are loosely coupled. Apps can be developed, updated, or removed independently.
*   **Discoverability:** The Core automatically finds and integrates compliant apps.
*   **Consistency:** Users get a consistent UI experience, as the Core handles the shell and apps contribute content and navigation in a structured way.
*   **Extensibility:** New functionalities can be easily added by developing new CIELO Apps.
*   **Security:** Navigation and access are driven by Django's permission system, ensuring users only see and access what they are authorized for.

## Demonstration Guide for Product Owners

This section outlines what has been implemented to showcase the dynamic app integration feature and what to expect when demonstrating it to stakeholders. The `inventory` app serves as the primary example of this integration.

### Implementation Summary

To enable dynamic app integration, the following key changes were made:

1.  **`inventory` App Refactoring:**
    *   The `inventory/apps.py` (`InventoryConfig`) was updated to declare `cielo_app_label`, `cielo_icon_class`, `cielo_navigation_provider`, and `cielo_permissions_provider`.
    *   A new file, `inventory/cielo_hooks.py`, was created. It contains:
        *   `get_navigation_items(request)`: This function defines the navigation links ("Virtual Machines", "Storage Accounts") that the `inventory` app wishes to expose. It checks user permissions before adding links.
        *   `get_app_permissions()`: This function lists the permissions the `inventory` app defines (e.g., `view_virtualmachine`).
    *   Basic models (`VirtualMachine`, `StorageAccount`) were added to `inventory/models.py`. This allows Django to automatically create standard permissions, which are then checked by `get_navigation_items`.

2.  **CIELO Core Enhancements:**
    *   A new context processor, `common.context_processors.cielo_navigation_context`, was created. This processor iterates through all installed apps, checks for the `cielo_navigation_provider` hook, and calls the specified function to collect navigation items.
    *   This context processor was registered in `cielo_core/settings.py` to make `cielo_navigation_items` available to all templates.
    *   The main layout template, `common/templates/common/base.html`, was modified to dynamically render the sidebar navigation by iterating over `cielo_navigation_items` instead of using hardcoded links.

### What to Demo and Expect

When demonstrating this feature, focus on how the CIELO Core integrates the `inventory` app's UI contributions seamlessly:

1.  **Dynamic Sidebar Navigation:**
    *   **Observe:** After logging in (e.g., as the `admin` user who has all permissions by default), the left sidebar will display links for "Virtual Machines" and "Storage Accounts". These links will have icons as defined in `inventory/cielo_hooks.py`.
    *   **Explain:** These navigation items are not hardcoded in the main `base.html` template. Instead, the `inventory` app *tells* the CIELO Core what links it wants to show. The Core then dynamically renders them. This demonstrates the pluggable nature of CIELO apps.

2.  **Permission-Based Visibility:**
    *   **Explain:** The `get_navigation_items` function in `inventory/cielo_hooks.py` uses `request.user.has_perm()` to decide whether to show a link. If a user does not have the `inventory.view_virtualmachine` permission, the "Virtual Machines" link will not appear for them. (This can be demonstrated by creating a test user with limited permissions via the Django admin).

3.  **App-Specific Content (Placeholder):**
    *   **Observe:** Clicking on "Virtual Machines" or "Storage Accounts" will navigate to the respective pages defined in the `inventory` app's `urls.py` and `views.py`.
    *   **Explain:** For this demonstration, the content of these pages is secondary. The `inventory` app currently does not fetch real data from any cloud provider. The views might show placeholder content, an empty table, or a "No items found" message. **The key takeaway is that the navigation to these app-specific views is managed dynamically by the Core based on the app's declared hooks.**

4.  **Decoupling:**
    *   **Explain:** This setup means new apps can be added to CIELO, and as long as they implement the `cielo_navigation_provider` hook, their navigation items will automatically appear in the sidebar without any changes to the CIELO Core's `base.html` template. This showcases the system's modularity and extensibility.

The goal of this demo is to illustrate the architectural pattern that allows CIELO to be extended with new functionalities (apps) that integrate smoothly into the main platform's UI. The `inventory` app, even with "fake" or no actual data, effectively demonstrates this powerful integration mechanism.