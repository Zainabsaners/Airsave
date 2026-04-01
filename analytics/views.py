from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import calculate_saving_metrics
from .models import SavingGoal

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