from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import datetime
from .models import SavingGoal, UserSavingsAnalytics
from .services import calculate_saving_metrics, get_system_wide_stats

class SavingGoalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all goals for the user"""
        goals = SavingGoal.objects.filter(user=request.user)
        return Response([{
            "id": g.id,
            "name": g.name,
            "target": g.target_amount,
            "current_saved": g.current_saved,
            "base": getattr(g, 'roundup_base', 10), # Default to 10 if field not migrated yet
            "is_active": getattr(g, 'is_active', True)
        } for g in goals])

    def post(self, request):
        """Create a new goal and set the rounding rule (Fixes 405 error)"""
        data = request.data
        
        # 1. Logic: Deactivate previous goals so the new one is the primary 'Active' one
        # (Assuming you added 'is_active' to your model as discussed)
        SavingGoal.objects.filter(user=request.user).update(is_active=False)

        # 2. Create the goal with the chosen rounding base (10, 50, or 100)
        goal = SavingGoal.objects.create(
            user=request.user,
            name=data.get('name', 'My Savings Goal'),
            target_amount=data.get('target_amount', 0),
            roundup_base=data.get('roundup_base', 10), 
            is_active=True
        )

        return Response({
            "message": "Goal created and rounding rule updated!",
            "goal": {
                "id": goal.id,
                "name": goal.name,
                "roundup_base": goal.roundup_base
            }
        }, status=status.HTTP_201_CREATED)

class ActiveGoalView(APIView):
    """Specific endpoint for the Dashboard to see the current saving strategy"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        goal = SavingGoal.objects.filter(user=request.user, is_active=True).first()
        if not goal:
            return Response({"goal": None})
        return Response({
            "goal": {
                "name": goal.name,
                "target": goal.target_amount,
                "saved": goal.current_saved,
                "base": goal.roundup_base
            }
        })

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        metrics = calculate_saving_metrics(request.user)
        goals = SavingGoal.objects.filter(user=request.user, is_active=True)
        
        goal_data = [{
            "name": goal.name,
            "target": goal.target_amount,
            "saved": goal.current_saved,
            "progress": (goal.current_saved / goal.target_amount) * 100 if goal.target_amount > 0 else 0,
            "base": goal.roundup_base
        } for goal in goals]

        return Response({
            "metrics": metrics,
            "goals": goal_data
        })

# ... keep SystemHealthView and SavingsSummaryView as they were ...
class SystemHealthView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = get_system_wide_stats()
        return Response({
            "system_status": "OPERATIONAL",
            "timestamp": datetime.now(),
            "financial_stats": stats,
        })
        
class SavingsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            stats = UserSavingsAnalytics.objects.get(user=request.user)
            return Response({
                "username": request.user.username,
                "total_airtime": stats.total_spent_on_airtime,
                "total_savings": stats.total_saved,
                "savings_ratio": f"{(stats.total_saved / (stats.total_saved + stats.total_airtime) * 100):.1f}%"
            })
        except UserSavingsAnalytics.DoesNotExist:
            return Response({"message": "No data yet. Start saving!"}, status=200)