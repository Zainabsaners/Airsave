import re

from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'password', 'email']
        # 1. Hide the password from responses for security
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, value):
        clean_value = re.sub(r'[\s\-\+]', '', value)
        pattern = r'^(?:254|0)(?:7|1)\d{8}$'
        if not re.match(pattern, clean_value):
            raise serializers.ValidationError(
                "Enter a valid Kenyan phone number (e.g., 07..., 01..., or 254...)"
            )
        return value

    # 2. Add this create method to fix the hashing issue
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', '')
        )
        return user
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims (Glen might need these in the React Frontend)
        token['phone_number'] = user.phone_number
        token['username'] = user.username
        return token
    
    
    
    