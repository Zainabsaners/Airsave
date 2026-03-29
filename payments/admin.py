from django.contrib import admin
from .models import MpesaTransaction # Example model name

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('checkout_request_id', 'phone_number', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('checkout_request_id', 'receipt_number')