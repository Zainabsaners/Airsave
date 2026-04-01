from django.urls import path
from .views import mpesa_callback, InitiateSTKPushView  

urlpatterns = [
    path('callback/', mpesa_callback, name='mpesa-callback'),
    path('initiate-stk-push/', InitiateSTKPushView.as_view(), name='initiate-stk-push'),
]