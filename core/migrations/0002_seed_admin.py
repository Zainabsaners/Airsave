from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_superuser(apps, schema_editor):
    # Get the User model dynamically
    User = apps.get_model('core', 'User') 
    
    # Check if they exist first to avoid errors on future deploys
    if not User.objects.filter(username='Airsave').exists():
        User.objects.create(
            username='Airsave',
            email='admin@airsave.com',
            phone_number='0702640917',
            password=make_password('cherotich@2005'), # Securely hash the password
            is_superuser=True,
            is_staff=True
        )

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'), # Must match your previous migration
    ]

    operations = [
        migrations.RunPython(create_initial_superuser),
    ]