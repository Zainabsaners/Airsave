from django.http import HttpResponseForbidden
from functools import wraps

# Safaricom's known Callback IP ranges (Example for Sandbox/Production)
SAFARICOM_IPS = [
    '196.201.214.200', 
    '196.201.214.206', 
    '196.201.213.114',
    '196.201.214.207',
    '127.0.0.1', # Allow localhost for testing with Ngrok
]

def whitelist_mpesa_ip(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get the real IP behind a proxy (like Ngrok or Render)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip not in SAFARICOM_IPS:
            # Trevor: Log this as a 'Suspicious Access Attempt' in AuditLogs
            print(f"SECURITY ALERT: Unauthorized Callback Attempt from {ip}")
            return HttpResponseForbidden("Access Denied")
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view