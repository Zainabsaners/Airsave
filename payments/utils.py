import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from decouple import config

class MpesaClient:
    def __init__(self):
        self.consumer_key = config('MPESA_CONSUMER_KEY')
        self.consumer_secret = config('MPESA_CONSUMER_SECRET')
        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    def get_access_token(self):
        """
        Fetches the OAuth2 token from Safaricom.
        """
        try:
            res = requests.get(
                self.auth_url, 
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
            )
            token = res.json()['access_token']
            return token
        except Exception as e:
            # Trevor: Log this as a security/connectivity error in AuditLogs later
            print(f"M-Pesa Token Error: {e}")
            return None
        
    def initiate_b2c_payout(self, phone, amount, command_id="BusinessPayment"):
        """
        Sends money from AirSave's M-Pesa Account to the User's Phone.
        """
        access_token = self.get_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        payload = {
            "InitiatorName": config('MPESA_INITIATOR_NAME'),
            "SecurityCredential": config('MPESA_SECURITY_CREDENTIAL'),
            "CommandID": command_id,
            "Amount": int(amount),
            "PartyA": config('MPESA_SHORTCODE'),
            "PartyB": phone,
            "Remarks": "AirSave Withdrawal",
            "QueueTimeOutURL": config('MPESA_B2C_TIMEOUT_URL'),
            "ResultURL": config('MPESA_B2C_RESULT_URL'),
            "Occasion": "Savings Withdrawal"
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()