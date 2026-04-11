import re
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

kenyan_phone_regex = RegexValidator(
    regex=r'^(?:\+254|254|0)?([71]\d{8})$',
    message="Phone number must be entered in the format: '0712345678' or '254712345678'. Up to 12 digits allowed."
)
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    # Standard Django login using username
    REQUIRED_FIELDS = ['email', 'phone_number'] 

    def save(self, *args, **kwargs):
        if self.phone_number:
            digits = re.sub(r'\D', '', self.phone_number)
            if digits.startswith('0'):
                self.phone_number = '254' + digits[1:]
            elif len(digits) == 9 and (digits.startswith('7') or digits.startswith('1')):
                self.phone_number = '254' + digits
            else:
                self.phone_number = digits
        super().save(*args, **kwargs)
class AuditLog(models.Model):
    """
    This is your security anchor. 
    It tracks every sensitive action in the system.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"