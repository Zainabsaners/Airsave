from django.db import models
from django.conf import settings

class MpesaTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 42 in the example
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    
    # 50 in the example (The actual STK Push amount)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    # The 'change' (8 in the example)
    savings_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    merchant_request_id = models.CharField(max_length=255, unique=True)
    checkout_request_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, SUCCESS, FAILED
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} ({self.status})"