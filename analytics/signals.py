from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import MpesaTransaction
from .models import UserSavingsAnalytics
from wallet.services import calculate_rounding_split, calculate_split

@receiver(post_save, sender=MpesaTransaction)
def update_user_analytics(sender, instance, created, **kwargs):
    if instance.status == 'SUCCESS':
        # Use our new logic
        split = calculate_rounding_split(instance.requested_amount)
        
        # Only update if there is actually something to record
        analytics, _ = UserSavingsAnalytics.objects.get_or_create(user=instance.user)
        analytics.total_spent_on_airtime += split["airtime_to_send"]
        analytics.total_saved += split["savings_amount"]
        analytics.save()