from django.db.models import Sum, Count
from wallet.models import Ledger
from decimal import Decimal

def calculate_saving_metrics(user):
    wallet = user.wallet
    
    # 1. Total Savings Lifetime
    total_saved = Ledger.objects.filter(
        wallet=wallet, 
        entry_type='ROUNDUP'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # 2. Saving Frequency (How many times they've rounded up)
    freq = Ledger.objects.filter(
        wallet=wallet, 
        entry_type='ROUNDUP'
    ).count()

    # 3. Discipline Score (Calculation: Savings frequency vs Withdrawals)
    withdrawals = Ledger.objects.filter(
        wallet=wallet, 
        entry_type='WITHDRAWAL'
    ).count()
    
    # Simple algorithm: Start at 100, subtract 10 for every withdrawal, 
    # add 5 for every 10 successful roundups.
    base_score = 70 
    discipline_score = base_score - (withdrawals * 10) + (freq // 10 * 5)
    
    # Cap between 0 and 100
    final_score = max(0, min(100, discipline_score))

    return {
        "total_saved": total_saved,
        "frequency": freq,
        "discipline_score": final_score
    }