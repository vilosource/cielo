reate a modular Django project named cielo using Poetry for dependency management.

This project is called CIELO – Cloud Infrastructure, Environment, and Lifecycle Orchestrator.
It is a multi-app Django project that will be rendered server-side using Bootstrap 5 and prepared for future REST API and React frontend integration.

The current directory is empty. Start from scratch and set up the project with best practices.

📦 Project Structure
swift
Copy
Edit
cielo/
├── pyproject.toml                     ← Poetry-managed project
├── manage.py
├── cielo_core/                        ← Main Django project (settings, URLs)
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── common/                            ← Shared templates, static files
│   ├── templates/common/base.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── logo/
├── inventory/                         ← App for virtual machines and storage accounts
│   └── templates/inventory/
│       ├── virtual_machines.html
│       └── storage_accounts.html
├── users/                             ← App for authentication
│   └── templates/users/login.html
⚙️ Setup Requirements
Use Poetry to manage dependencies

Install Django

Initialize Django project as cielo_core

Create Django apps:

common: layout, base templates, shared static files

inventory: for infrastructure inventory views

users: for authentication (login/logout/profile)

Add apps to INSTALLED_APPS

Use Django’s built-in LoginView and LogoutView

🎨 UI and Theming
Use Bootstrap 5 (via CDN or static include)

Use this color palette:

Primary blue: #0076C0

Accent orange: #F5A623

Neutral gray: #4A4A4A

Support client-side light/dark theme toggle

Ensure all templates are responsive and use semantic HTML5

🧩 Templates to Implement
common/templates/common/base.html

Fixed left sidebar:

Links: “Virtual Machines”, “Storage Accounts”

Top navbar:

Project name: CIELO

Tagline: Cloud Infrastructure, Environment, and Lifecycle Orchestrator

Light/dark theme toggle

User profile dropdown (shows username, “Settings”, “Logout”)

Uses {% block content %} for inner pages

inventory/templates/inventory/virtual_machines.html

Heading: Virtual Machines

Summary cards (e.g., total VMs)

Bootstrap table: Name, Location, Environment

inventory/templates/inventory/storage_accounts.html

Heading: Storage Accounts

Table: Name, Location, SKU, Access Tier

users/templates/users/login.html

Clean login form with Bootstrap styling

Centered form with CIELO name and tagline

POSTs to Django's login view

🔐 Auth & Access
Use Django’s LoginView and LogoutView

Add URLs for /login/ and /logout/

Protect inventory views with @login_required

Show user menu in navbar only if user.is_authenticated

🌱 Extensibility
Layout and template structure should allow future:

REST API integration

React frontend using the same API

Markdown wiki

Dashboard charts via Chart.js
