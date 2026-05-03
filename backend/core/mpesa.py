import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from datetime import datetime
import base64

class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.base_url = "https://sandbox.safaricom.co.ke"

    def get_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        return response.json().get('access_token')

    def stk_push(self, phone, amount, reference):
        token = self.get_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Generate Password: base64(shortcode + passkey + timestamp)
        password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone, # Customer phone
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": reference,
            "TransactionDesc": "Airsave Micro-savings"
        }

        headers = {"Authorization": f"Bearer {token}"}
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        
        response = requests.post(url, json=payload, headers=headers)
        return response.json()