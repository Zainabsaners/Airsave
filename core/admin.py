from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuditLog

# Since we use phone_number as the username, we customize the admin display
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'username', 'email', 'is_verified', 'is_staff')
    search_fields = ('phone_number', 'email')
    ordering = ('phone_number',)

admin.site.register(User, CustomUserAdmin)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    readonly_fields = ('timestamp',) # Security: Don't allow editing of logs
