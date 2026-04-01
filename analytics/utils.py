from wallet.models import Ledger
from django.db.models import Sum

def get_user_saving_velocity(user):
    """
    Calculates how much a user saves per airtime transaction on average.
    """
    total_saved = Ledger.objects.filter(
        wallet__user=user, 
        entry_type='ROUNDUP'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return total_saved