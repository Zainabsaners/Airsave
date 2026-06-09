from django.urls import path
from .views import (
    DashboardAnalyticsView, 
    SavingGoalView, 
    ActiveGoalView, 
    SavingsSummaryView, 
    SystemHealthView
)

urlpatterns = [
    # GET to list, POST to create (This matches api/goals/ in your frontend)
    path('', SavingGoalView.as_view(), name='goal-list-create'),
    
    # Matches api/goals/active/
    path('active/', ActiveGoalView.as_view(), name='active-goal'),
    
    # Analytics
    path('dashboard/', DashboardAnalyticsView.as_view(), name='dashboard-stats'),
    path('summary/', SavingsSummaryView.as_view(), name='savings-summary'),
    path('health/', SystemHealthView.as_view(), name='system-health'),
]