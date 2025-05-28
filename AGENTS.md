# CIELO Developer Guide

## Project Overview

CIELO (Cloud Infrastructure, Environment, and Lifecycle Orchestrator) is a modular Django platform designed to manage and orchestrate cloud resources across multiple providers. The project follows a pluggable architecture where core services are separated from specialized functionality through independent "CIELO Apps."

### Key Features Summary

- **Cloud-Agnostic Core Platform**: Provides authentication, authorization, session management, and UI shell
- **Pluggable Application Architecture**: Specialized functionalities implemented as independent Django apps
- **Dynamic App Integration**: Apps declare their integration points (permissions, navigation) to the core
- **Responsive Material Design UI**: Built with Bootstrap 5 and a professional admin theme
- **Server-Side Rendering**: Django templates with modern, responsive layouts

## Project Architecture

### Core Components

- **`cielo_core/`**: Main Django project with settings, URLs, and WSGI configuration
- **`common/`**: Shared utilities, base templates, static assets, and context processors
- **`inventory/`**: Example CIELO app demonstrating cloud resource management
- **`users/`**: Authentication and user management
- **`material/`**: Design reference templates from the Minton admin theme

### CIELO App Integration System

CIELO apps integrate with the core through a standardized hook system:

1. **App Configuration**: Apps declare integration points in their `apps.py`:
   ```python
   class InventoryConfig(AppConfig):
       cielo_app_label = _("Inventory")
       cielo_icon_class = "bi-archive"
       cielo_navigation_provider = "inventory.cielo_hooks.get_navigation_items"
       cielo_permissions_provider = "inventory.cielo_hooks.get_app_permissions"
   ```

2. **Navigation Providers**: Apps provide navigation items through hook functions:
   ```python
   def get_navigation_items(request):
       items = []
       if request.user.has_perm('inventory.view_virtualmachine'):
           items.append({
               'label': _('Virtual Machines'),
               'url': reverse('inventory:virtual_machines'),
               'icon_class': 'bi-hdd-stack',
               'active_pattern_names': ['inventory:virtual_machines'],
           })
       return items
   ```

3. **Context Processor**: The `cielo_navigation_context` processor aggregates navigation from all apps and makes it available in templates.

## Template System and UI Framework

### Base Template: `base_material.html`

The core UI is built around `common/templates/common/base_material.html`, which provides:

- **Responsive Layout**: Fixed left sidebar, top navigation, main content area
- **Theme Integration**: Professional admin theme with light/dark mode support
- **Dynamic Navigation**: Automatically populated from registered CIELO apps
- **User Authentication UI**: Login status, user dropdown, permissions-based content
- **Extensible Blocks**: Multiple template blocks for customization

#### Key Template Blocks

```html
{% block title %}{% endblock %}           <!-- Browser title -->
{% block page_title %}{% endblock %}     <!-- Main page heading -->
{% block breadcrumb %}{% endblock %}     <!-- Breadcrumb navigation -->
{% block content %}{% endblock %}        <!-- Main content area -->
{% block extra_head %}{% endblock %}     <!-- Additional CSS/meta tags -->
{% block extra_js %}{% endblock %}       <!-- Additional JavaScript -->
```

#### Navigation System

The base template includes a dynamic sidebar that automatically displays navigation items from all registered CIELO apps:

```html
<div id="sidebar-menu">
    <ul id="side-menu">
        <li class="menu-title">CIELO Navigation</li>
        {% for item in cielo_navigation_items %}
            {% if item.sub_items %}
                <!-- Expandable menu with sub-items -->
            {% else %}
                <!-- Single navigation item -->
            {% endif %}
        {% endfor %}
    </ul>
</div>
```

### Using Material Design References

The `material/` directory contains comprehensive HTML templates from the Minton admin theme. These serve as design references and component libraries for building CIELO pages.

#### How to Use Material Templates

1. **Browse Available Designs**: The `material/` directory contains over 100 pre-built pages:
   - `dashboard-*.html`: Various dashboard layouts
   - `tables-*.html`: Different table styles and interactions
   - `forms-*.html`: Form layouts and components
   - `ui-*.html`: UI components (buttons, cards, modals, etc.)
   - `charts-*.html`: Chart and visualization examples

2. **Extract Components**: Copy relevant HTML sections from material templates:
   ```html
   <!-- From material/tables-basic.html -->
   <div class="card">
       <div class="card-body">
           <h4 class="header-title">Your Table Title</h4>
           <table class="table table-striped">
               <!-- Table content -->
           </table>
       </div>
   </div>
   ```

3. **Adapt for Django**: Convert to Django template syntax:
   ```html
   <!-- In your CIELO app template -->
   {% extends 'common/base_material.html' %}
   
   {% block content %}
   <div class="card">
       <div class="card-body">
           <h4 class="header-title">{{ page_title }}</h4>
           <table class="table table-striped">
               {% for item in object_list %}
                   <tr>
                       <td>{{ item.name }}</td>
                   </tr>
               {% endfor %}
           </table>
       </div>
   </div>
   {% endblock %}
   ```

#### Static Assets

The material theme assets are integrated into Django's static file system:
- **Location**: `common/static/material_theme/`
- **Usage**: Reference via `{% static 'material_theme/css/app.min.css' %}`
- **Components**: CSS, JavaScript, images, fonts, and icons

## Development Best Practices

### Creating a New CIELO App

1. **Generate Django App**:
   ```bash
   python manage.py startapp your_app_name
   ```

2. **Configure App Integration** in `apps.py`:
   ```python
   class YourAppConfig(AppConfig):
       name = 'your_app_name'
       cielo_app_label = _("Your App")
       cielo_icon_class = "bi-your-icon"
       cielo_navigation_provider = "your_app_name.cielo_hooks.get_navigation_items"
   ```

3. **Create Hook Functions** in `cielo_hooks.py`:
   ```python
   def get_navigation_items(request):
       return [{
           'label': _('Your Feature'),
           'url': reverse('your_app_name:your_view'),
           'icon_class': 'bi-your-icon',
       }]
   ```

4. **Register in Settings**:
   ```python
   INSTALLED_APPS = [
       # ... other apps
       'your_app_name',
   ]
   ```

### Template Development

1. **Extend Base Template**:
   ```html
   {% extends 'common/base_material.html' %}
   ```

2. **Use Material Components**: Reference `material/` templates for styling patterns

3. **Implement Required Blocks**:
   ```html
   {% block title %}Your Page Title{% endblock %}
   {% block page_title %}Your Page Title{% endblock %}
   {% block content %}
       <!-- Your page content -->
   {% endblock %}
   ```

### Navigation and Permissions

- Use Django's permission system for access control
- Navigation items automatically respect user permissions
- Test with different user roles to ensure proper access restrictions

### Static File Management

- Place app-specific static files in `your_app/static/your_app/`
- Use `{% static %}` template tag for all asset references
- Run `python manage.py collectstatic` for production deployments

## Getting Started

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access Application**: Navigate to `http://localhost:8000`

## Available Material Components

The `material/` directory provides extensive examples for:

- **Dashboards**: Analytics, CRM layouts
- **Tables**: Basic, DataTables, responsive, editable
- **Forms**: Basic, advanced, validation, file uploads
- **Charts**: Apex, Chart.js, Morris, and more
- **UI Components**: Cards, buttons, modals, tooltips
- **Authentication**: Login, register, password recovery
- **E-commerce**: Products, orders, customers
- **Communication**: Email, chat, calendar

Use these as references to build consistent, professional interfaces for your CIELO applications.
