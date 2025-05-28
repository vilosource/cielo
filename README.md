# CIELO

CIELO, which stands for **Cloud Infrastructure, Environment, and Lifecycle Orchestrator**, is a modular Django project designed to manage and orchestrate cloud resources.
It serves as a foundational platform, providing core services like user management, a consistent UI shell, and security, while allowing specialized "CIELO Apps" to be plugged in for specific functionalities.

This project currently provides a server-rendered web interface built with Django and Bootstrap 5. It features a responsive layout with a fixed sidebar, top navigation bar, and a light/dark theme toggle. Initial functionalities include:
- Basic inventory management examples (e.g., for generic Virtual Machines and Storage Accounts).
- User authentication (login/logout) using Django's built-in system.

## Key Features

*   **Cloud-Agnostic Core Platform:**
    *   CIELO Core provides essential services: user authentication, authorization, session management, and the overall UI shell (base templates, navigation structure).
    *   The Core is designed to be independent of any specific cloud provider.
*   **Pluggable Application Architecture:**
    *   Specialized functionalities (e.g., managing Azure VMs, AWS S3 buckets, GCP Compute Engines) are implemented as independent "CIELO Apps."
    *   Apps are self-contained Django applications that define their own models, views, and logic.
*   **Dynamic App Integration & UI Contribution:**
    *   CIELO Apps declare their integration points to the Core, such as permissions they define and navigation items they wish to expose.
    *   The Core dynamically discovers and integrates these apps.
    *   Apps can contribute rich, hierarchical navigation structures to the main UI. For example, an `azure_vms_inventory` app could provide a menu allowing users to browse through Azure subscriptions, then resource groups, and finally view VMs within a selected group, all rendered within the Core's standard navigation panels.
*   **Example Inventory Modules:**
    *   Includes basic, illustrative modules for inventory management (e.g., `inventory` app for generic VMs and storage accounts) that demonstrate the app integration principles.
*   **User Authentication:**
    *   Secure user login and logout powered by Django's `LoginView` and `LogoutView`.
    *   Protected views requiring user authentication (`@login_required`).
*   **Responsive UI & Theming:**
    *   Built with Bootstrap 5 for a responsive experience across devices.
    *   Client-side light/dark theme toggle.
    *   Consistent layout with a fixed left sidebar and a top navigation bar.
*   **Server-Side Rendering:** Initial interface rendered using Django templates, providing a solid foundation.

## Project Structure

The project is organized into several Django apps:

*   `cielo_core/`: The main Django project directory containing settings, main URL configurations, and WSGI application.
*   `common/`: Houses shared resources like base templates (`base.html`), common static files (CSS, JS, logos), and global navigation elements.
*   `users/`: Handles user authentication, profiles, and related functionalities.
*   `inventory/` (example app): A sample app demonstrating basic inventory management (e.g., Virtual Machines, Storage Accounts) and integration with the CIELO Core.
*   **(Future CIELO Apps):** Additional apps (e.g., `azure_vms_inventory`, `aws_s3_manager`) would follow a similar structure, plugging into the CIELO Core.

## Future Vision

CIELO is designed with extensibility in mind. Future enhancements include:

*   **Expanding Ecosystem of CIELO Apps:** Development of more sophisticated apps for various cloud services and operational tasks.
*   **Comprehensive REST API:** To enable programmatic access and support a decoupled frontend.
*   **Dynamic React Frontend:** Transitioning to or augmenting with a modern React-based user interface.
*   **Enhanced Core Services:** Such as centralized credential management for apps, advanced auditing, and a richer dashboarding framework.
*   **Markdown-based Wiki:** Integrating a wiki system for documentation and knowledge sharing within the platform.
*   **Advanced Dashboarding:** Implementing interactive dashboards using libraries like Chart.js for data visualization.

## Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/)

## Setup

1. Clone this repository.
2. Install dependencies with `poetry install`.
3. Optional: create an admin user with `poetry run python manage.py createsuperuser`.
   On first run the project automatically creates a default administrator with
   username `admin` and password `admin`. When logging in with these defaults you
   will be required to change the password unless the environment variable
   `CIELO_DEPLOYMENT` is set to `development` or `dev`.

## Running the Demo

A helper script `start_demo.sh` is included to initialize the project and launch the development server.

```bash
./start_demo.sh
```

The script will run database migrations and start the Django site at http://localhost:8000/. After it starts, open your browser and visit that URL to explore the demo.
