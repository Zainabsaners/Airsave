import uuid
from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # We store a 'cached' balance for fast reading, but the Ledger is the source of truth
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number}'s Wallet"

class Ledger(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('ROUNDUP', 'Round-up Saving'),
        ('WITHDRAWAL', 'Withdrawal'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='entries')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # Security: Reference to the external M-Pesa Transaction ID
    reference_id = models.CharField(max_length=100, unique=True) 
    
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entry_type} - {self.amount} ({self.wallet.user.phone_number})"
    
class WithdrawalRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount} ({self.status})"