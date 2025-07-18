from rest_framework import serializers
from .models import CustomUser, CustomerVerification
from django.contrib.auth import get_user_model
from .models import UserRating
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomerVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerVerification
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'is_owner', 'password', 'confirm_password']

    def validate_email(self, value):
        # Format validation
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email format.")

        # Uniqueness validation
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")

        return value
    
    def validate_username(self, value):

        # Uniqueness check
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use.")

        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['id', 'user', 'rating', 'created_at', 'updated_at']

class LoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField()

class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    

