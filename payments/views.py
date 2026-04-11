import base64
from datetime import datetime
import requests
import json
from decimal import Decimal

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from decouple import config

from .utils import MpesaClient
from .models import MpesaTransaction
from wallet.models import Wallet, Ledger
from .security import whitelist_mpesa_ip
from wallet.services import calculate_split # Ensure you created this service
from rest_framework.permissions import IsAuthenticated

# --- Mock Telecom Service ---
def call_telecom_provider_api(phone, amount):
    """
    Simulates sending airtime. 
    In a real app, this would be an API call to Safaricom/Airtel.
    """
    print(f"DEBUG: Sending {amount} KES airtime to {phone}")
    return True # Simulate success

class InitiateSTKPushView(APIView):
    # Ensure this is set so request.user works
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        # 1. Get data from request
        phone = request.data.get('phone')
        amount = request.data.get('amount')
        
        if not phone or not amount:
            return Response({"error": "Phone and amount are required"}, status=400)

        # 2. Use the Client we already built
        client = MpesaClient()
        # Pass phone, amount, and a unique reference
        res_data = client.stk_push(phone, amount, f"AirSave_{request.user.username}")

        # 3. Handle the response and save to DB
        if res_data.get('ResponseCode') == '0':
            MpesaTransaction.objects.create(
                user=request.user,
                phone_number=phone,
                amount=Decimal(amount),
                checkout_request_id=res_data.get('CheckoutRequestID'),
                status='PENDING'
            )
            return Response({"message": "STK Push initiated", "checkout_id": res_data.get('CheckoutRequestID')})
        
        return Response({"error": "Safaricom rejected the request", "details": res_data}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
@whitelist_mpesa_ip
def mpesa_callback(request):
    data = request.data
    stk_callback = data['Body']['stkCallback']
    result_code = stk_callback['ResultCode']
    checkout_request_id = stk_callback['CheckoutRequestID']

    try:
        mpesa_tx = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
    except MpesaTransaction.DoesNotExist:
        return Response({"ResultCode": 1, "ResultDesc": "Internal Error"})

    if result_code == 0:
        callback_metadata = stk_callback['CallbackMetadata']['Item']
        receipt = next(item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber')
        
        # --- THE SPLIT LOGIC START ---
        # 1. Calculate how much is Airtime vs Savings
        # Example: User paid 50. Airtime = 47, Savings = 3.
        airtime_amount, savings_amount = calculate_split(mpesa_tx.amount)

        try:
            with transaction.atomic():
                # 2. Update M-Pesa Record
                mpesa_tx.status = 'SUCCESS'
                mpesa_tx.receipt_number = receipt
                mpesa_tx.save()

                # 3. Credit the Wallet Ledger (ONLY the savings part)
                wallet = Wallet.objects.select_for_update().get(user=mpesa_tx.user)
                
                Ledger.objects.create(
                    wallet=wallet,
                    amount=savings_amount,
                    entry_type='ROUNDUP',
                    reference_id=f"SAV-{receipt}",
                    description=f"Savings from {mpesa_tx.amount} purchase"
                )

                # 4. Update the Wallet Balance
                wallet.balance += savings_amount
                wallet.save()

                # 5. TRIGGER AIRTIME DISPATCH
                # If this fails, the whole transaction (Wallet credit) rolls back!
                airtime_success = call_telecom_provider_api(mpesa_tx.phone_number, airtime_amount)
                
                if not airtime_success:
                    raise Exception("Telecom Provider API Failed")

        except Exception as e:
            # Trevor: In production, log this critical failure for manual intervention
            return Response({"ResultCode": 1, "ResultDesc": "Split Logic Failed"})

    else:
        mpesa_tx.status = 'FAILED'
        mpesa_tx.save()

    return Response({"ResultCode": 0, "ResultDesc": "Success"})