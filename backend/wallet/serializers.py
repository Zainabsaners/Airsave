from rest_framework import serializers
from .models import Wallet, Ledger

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'created_at']

class RoundUpCalculationSerializer(serializers.Serializer):
    # This is for the 'input' from the frontend
    original_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    rounding_base = serializers.IntegerField(default=10) # 10, 50, or 100

    # These are the 'output' fields
    roundup_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_to_pay = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)