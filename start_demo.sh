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

# Start the development server
echo "Starting CIELO at http://localhost:8000/"
poetry run python manage.py runserver 0.0.0.0:8000

