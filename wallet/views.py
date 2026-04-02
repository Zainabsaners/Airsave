from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
import math
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, Ledger, WithdrawalRequest
from .serializers import WalletSerializer
from django.db import transaction
from payments.utils import MpesaClient
from core.models import AuditLog
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

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated] # 🔒 Security: Block unauthenticated access

    def get(self, request):
        # We fetch the wallet specifically tied to the logged-in user
        user = request.user
        wallet = Wallet.objects.get(user=user)
        
        # Get recent savings (Analytics)
        recent_savings = Ledger.objects.filter(
            wallet=wallet, 
            entry_type='ROUNDUP'
        ).order_by('-timestamp')[:5]

        return Response({
            "profile": {
                "phone_number": user.phone_number,
                "username": user.username,
                "is_verified": user.is_verified,
            },
            "wallet": {
                "balance": wallet.balance,
                "total_transactions": Ledger.objects.filter(wallet=wallet).count()
            },
            "recent_activity": [
                {
                    "amount": entry.amount,
                    "date": entry.timestamp,
                    "ref": entry.reference_id
                } for entry in recent_savings
            ]
        })
        
class WithdrawFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = Decimal(request.data.get('amount', 0))
        user = request.user

        if amount < 10: # Minimum withdrawal rule
            return Response({"error": "Minimum withdrawal is 10 KES"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. LOCK the wallet row for the duration of this logic
                wallet = Wallet.objects.select_for_update().get(user=user)

                # 2. Verify Funds
                if wallet.balance < amount:
                    return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

                # 3. Create Pending Withdrawal Record
                withdrawal = WithdrawalRequest.objects.create(user=user, amount=amount)

                # 4. Deduct immediately (Optimistic Locking)
                # If M-Pesa fails later, we will have a 'Reversal' logic
                wallet.balance -= amount
                wallet.save()

                # 5. Record in Ledger
                Ledger.objects.create(
                    wallet=wallet,
                    amount=amount,
                    entry_type='WITHDRAWAL',
                    reference_id=f"WDL-{withdrawal.id}",
                    description=f"Withdrawal to {user.phone_number}"
                )

                # 6. Trigger M-Pesa B2C
                client = MpesaClient()
                mpesa_response = client.initiate_b2c_payout(user.phone_number, amount)
                
                AuditLog.objects.create(
                    user=user,
                    action="WITHDRAWAL_INITIATED",
                    ip_address=request.META.get('REMOTE_ADDR'),
                    details={"amount": str(amount), "status": "PENDING"}
                )

                return Response({
                    "message": "Withdrawal initiated. You will receive an M-Pesa message shortly.",
                    "request_id": withdrawal.id,
                    "mpesa_status": mpesa_response
                })
    

        except Exception as e:
            return Response({"error": "System error during withdrawal"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)