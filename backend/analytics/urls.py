from django.urls import path
from .views import DashboardAnalyticsView, SystemHealthView

urlpatterns = [
    path('dashboard/', DashboardAnalyticsView.as_view(), name='dashboard-analytics'),
    path('health/', SystemHealthView.as_view(), name='system-health'), # This will be /api/analytics/health/
]