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