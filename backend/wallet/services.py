from decimal import Decimal
import math

def calculate_rounding_split(requested_airtime):
    """
    Option A: Round up to nearest 10. 
    If already a multiple of 10, savings = 0.
    """
    # If it's already 50, 50 % 10 is 0. 
    # If it's 42, 42 % 10 is 2.
    remainder = requested_airtime % 10
    
    if remainder == 0:
        total_to_charge = requested_airtime
        savings = 0
    else:
        # Standard round up: 42 -> 50
        total_to_charge = math.ceil(requested_airtime / 10.0) * 10
        savings = total_to_charge - requested_airtime
    
    return {
        "total_m_pesa_charge": total_to_charge,
        "airtime_to_send": requested_airtime,
        "savings_amount": savings
    }