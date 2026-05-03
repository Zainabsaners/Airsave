
# Register your models here.
from django.contrib import admin
from .models import Wallet, Ledger

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at')
    search_fields = ('user__phone_number',)

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'entry_type', 'reference_id', 'timestamp')
    list_filter = ('entry_type', 'timestamp')
    search_fields = ('reference_id', 'wallet__user__phone_number')