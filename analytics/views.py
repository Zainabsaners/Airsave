from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import calculate_saving_metrics
from .models import SavingGoal
from rest_framework.permissions import IsAdminUser # 🔒 Only Staff/Admins
from .services import get_system_wide_stats
from datetime import datetime

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        metrics = calculate_saving_metrics(request.user)
        
        # Fetch active goals
        goals = SavingGoal.objects.filter(user=request.user)
        goal_data = [{
            "name": goal.name,
            "target": goal.target_amount,
            "saved": goal.current_saved,
            "progress": (goal.current_saved / goal.target_amount) * 100 if goal.target_amount > 0 else 0
        } for goal in goals]

        return Response({
            "metrics": metrics,
            "goals": goal_data
        })
        
class SystemHealthView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = get_system_wide_stats()
        return Response({
            "system_status": "OPERATIONAL",
            "timestamp": datetime.now(),
            "financial_stats": stats,
        })