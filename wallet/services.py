from decimal import Decimal

def get_roundup_amount(transaction_amount):
    """
    Calculates the roundup to the nearest 10.
    Example: 43.00 -> Roundup is 7.00 (Total 50)
    """
    amount = Decimal(str(transaction_amount))
    if amount % 10 == 0:
        return Decimal('0.00')
    
    next_ten = ((amount // 10) + 1) * 10
    return next_ten - amount