from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuditLog
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    list_display = ('username', 'phone_number', 'email', 'is_verified')
    search_fields = ('username', 'phone_number', 'email')
    
    # This is the "Add User" page layout
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'email', 'password1', 'password2'),
        }),
    )

    # This is the "Edit User" page layout
    fieldsets = (
        ('Account Credentials', {'fields': ('username', 'password')}),
        ('Mobile Savings Info', {'fields': ('phone_number', 'is_verified')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')