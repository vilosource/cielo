# CIELO

CIELO (Cloud Infrastructure, Environment, and Lifecycle Orchestrator) is a modular Django project.

This bootstrap provides a server-rendered interface using Bootstrap 5 and prepares the project for future API and React frontend integration.

## Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/)

## Setup

1. Clone this repository.
2. Install dependencies with `poetry install`.
3. Optional: create an admin user with `poetry run python manage.py createsuperuser`.

## Running the Demo

A helper script `start_demo.sh` is included to initialize the project and launch the development server.

```bash
./start_demo.sh
```

The script will run database migrations and start the Django site at http://localhost:8000/. After it starts, open your browser and visit that URL to explore the demo.

