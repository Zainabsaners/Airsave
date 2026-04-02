from django.db.models import Sum, Count
from wallet.models import Ledger, Wallet
from payments.models import MpesaTransaction
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
    
def get_system_wide_stats():
    # 1. Total Liability (The sum of all user balances)
    total_user_balances = Wallet.objects.aggregate(Sum('balance'))['balance__sum'] or Decimal('0.00')

    # 2. Total Airtime Volume (Gross transaction volume)
    total_volume = MpesaTransaction.objects.filter(status='SUCCESS').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # 3. Total Savings Captured (Sum of all Round-ups)
    total_savings = Ledger.objects.filter(entry_type='ROUNDUP').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # 4. System Liquidity Check
    # In a real scenario, you'd compare this to your M-Pesa API balance
    return {
        "total_liability": total_user_balances,
        "total_airtime_processed": total_volume,
        "total_savings_trapped": total_savings,
        "active_users": Wallet.objects.count(),
    }