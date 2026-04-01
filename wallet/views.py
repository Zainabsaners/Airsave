from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
import math

class RoundUpPreviewView(APIView):
    """
    Endpoint: /api/wallet/preview-roundup/
    Purpose: Let the user see the savings before they click 'Pay'
    """
    def post(self, request):
        amount = Decimal(request.data.get('amount', 0))
        base = int(request.data.get('base', 10)) # Default to nearest 10

        if amount <= 0:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        # The Rounding Algorithm
        next_multiple = Decimal(math.ceil(amount / base) * base)
        if next_multiple == amount:
            # If they buy exactly 50, we might suggest rounding to 60 or 100
            next_multiple = amount + Decimal(base)
            
        savings = next_multiple - amount

        return Response({
            "original_airtime": amount,
            "savings_contribution": savings,
            "total_m_pesa_charge": next_multiple,
            "message": f"You are saving KES {savings} with this purchase!"
        })