import re

from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'password', 'email']

    def validate_phone_number(self, value):
        # Clean the input to check length
        clean_value = re.sub(r'[\s\-\+]', '', value)
        
        # Check if it matches Kenyan patterns (07..., 01..., 2547..., 2541...)
        pattern = r'^(?:254|0)(?:7|1)\d{8}$'
        if not re.match(pattern, clean_value):
            raise serializers.ValidationError(
                "Enter a valid Kenyan phone number (e.g., 07..., 01..., or 254...)"
            )
        return value
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims (Glen might need these in the React Frontend)
        token['phone_number'] = user.phone_number
        token['username'] = user.username
        return token