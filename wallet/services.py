from decimal import Decimal
import math

def calculate_split(total_paid, base=10):
    """
    Logic: The user pays a round number (e.g., 50). 
    We find the 'Actual Airtime' by subtracting the roundup.
    
    Example 1: Paid 50. Nearest 10 below 50 is 40? No. 
    In your team's model: 47 becomes 50. So if they paid 50, 
    the savings is 3 and airtime is 47.
    """
    total = Decimal(str(total_paid))
    
    # We define a standard 'Micro-saving' buffer. 
    # If they pay 50, we can use a rule like 5% or 
    # a fixed 'remainder' logic.
    
    # Common Rounding Rule for AirSave:
    # Savings = total_paid % base. 
    # If remainder is 0 (e.g., 50), we take a default small amount (e.g., 2 KES)
    # so they always save something.
    
    savings = total % Decimal(str(base))
    
    if savings == 0:
        savings = Decimal('2.00') # Default "Nudge" if they pay exactly 10, 20, 50
        
    airtime_value = total - savings
    
    return airtime_value, savings