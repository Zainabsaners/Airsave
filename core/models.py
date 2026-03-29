from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # Field for M-Pesa phone number (e.g., 254712345678)
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        db_index=True,
        help_text=_("Enter phone number in format 2547XXXXXXXX")
    )
    
    # KYC and Security flags
    is_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    
    # We use phone_number for authentication
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.phone_number

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