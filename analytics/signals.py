from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import MpesaTransaction
from .models import UserSavingsAnalytics
from wallet.services import calculate_split

@receiver(post_save, sender=MpesaTransaction)
def update_user_analytics(sender, instance, created, **kwargs):
    # Only update if the transaction just moved to SUCCESS status
    if instance.status == 'SUCCESS':
        airtime, savings = calculate_split(instance.amount)
        
        analytics, _ = UserSavingsAnalytics.objects.get_or_create(user=instance.user)
        analytics.total_spent_on_airtime += airtime
        analytics.total_saved += savings
        analytics.save()