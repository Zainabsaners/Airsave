#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# This will print the live users to your Render Logs so you can see them!
echo "--- STARTING LIVE USER LIST ---"
python manage.py shell -c "
from core.models import User;

users = User.objects.all();

print('===== USERS =====');

for u in users:
    print({
        'username': u.username,
        'email': u.email,
        'is_superuser': u.is_superuser,
        'is_staff': u.is_staff
    });

print('===== END USERS =====');
"
echo "--- ENDING LIVE USER LIST ---"