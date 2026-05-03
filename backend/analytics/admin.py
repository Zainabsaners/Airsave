from django.contrib import admin
from .models import SavingGoal

@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'target_amount', 'current_saved', 'is_completed')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('name', 'user__phone_number')