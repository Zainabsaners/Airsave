from django.urls import path
from .views import RoundUpPreviewView, WithdrawFundsView

urlpatterns = [
    path('preview-roundup/', RoundUpPreviewView.as_view(), name='preview-roundup'),
    path('preview/', RoundUpPreviewView.as_view(), name='preview-roundup'), 
    path('withdraw/', WithdrawFundsView.as_view(), name='withdraw-funds'),
]