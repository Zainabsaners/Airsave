from django.contrib import admin
from .models import MpesaTransaction # Example model name

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.short_description = 'User Phone'
    
    list_display = ('checkout_request_id', 'phone_number', 'requested_amount','total_amount', 'savings_amount', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('checkout_request_id', 'receipt_number')