#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# This line creates the admin automatically if it doesn't exist
python manage.py createsuperuser --no-input || echo "Superuser already exists"