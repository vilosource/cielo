#!/bin/bash
set -e

# Ensure poetry is installed
if ! command -v poetry >/dev/null 2>&1; then
  echo "Poetry is required. Please install it first." >&2
  exit 1
fi

# Install dependencies
poetry install

# Apply database migrations
poetry run python manage.py migrate --noinput

# Populate database with sample inventory data
poetry run python manage.py populate_inventory_data

# Set deployment environment to development to bypass forced password change for default admin
export CIELO_DEPLOYMENT=development

# Start the development server
echo "Starting CIELO at http://localhost:8000/"
poetry run python manage.py runserver 0.0.0.0:8000
