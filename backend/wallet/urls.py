from django.urls import path
from .views import (
    RoundUpPreviewView, WithdrawFundsView, 
    UserProfileView, GoalsListView, NotificationListView
)

urlpatterns = [
    path('', UserProfileView.as_view(), name='wallet-detail'), 
    path('preview-roundup/', RoundUpPreviewView.as_view()),
    path('withdraw/', WithdrawFundsView.as_view()),
    path('goals/', GoalsListView.as_view()),
    path('notifications/', NotificationListView.as_view()),
]