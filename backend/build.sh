#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# This will print the live users to your Render Logs so you can see them!
echo "--- STARTING LIVE USER LIST ---"
python manage.py shell -c "
from django.contrib.auth import get_user_model;

User = get_user_model();

if not User.objects.filter(username='Airsave').exists():
    User.objects.create_superuser(
        username='Airsave',
        email='airsave@gmail.com',
        password='Airsave@123'
    );
    print('Superuser created');
else:
    print('Superuser already exists');
"