#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# This will print the live users to your Render Logs so you can see them!
echo "--- STARTING LIVE USER LIST ---"
python manage.py shell -c "from core.models import User; print([(u.username, u.is_superuser) for u in User.objects.all()])"
echo "--- ENDING LIVE USER LIST ---"