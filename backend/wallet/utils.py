import math

def calculate_airsave_roundup(amount, base=10):
    """
    Calculates the difference to the nearest base (10, 50, or 100).
    Example: 43 rounded to nearest 50 = 7 savings.
    """
    if amount % base == 0:
        return 0
    next_multiple = math.ceil(amount / base) * base
    return next_multiple - amount