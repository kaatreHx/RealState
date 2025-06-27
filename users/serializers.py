from rest_framework import serializers
from .models import CustomUser, CustomerVerification
from django.contrib.auth import get_user_model
from .models import UserRating
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'is_owner', 'is_staff', 'is_active', 'is_online', 'created_at', 'updated_at']

class CustomerVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerVerification
        fields = ['id', 'user', 'first_name', 'last_name', 'dob', 'gender', 'profile_image', 'address', 'city', 'country', 'postal_code', 'document_type', 'document_number', 'document_front', 'document_back', 'is_verified', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'is_owner', 'password', 'confirm_password']

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
    
    def validate_phone(self, value):
        # Format: simple regex for 10-15 digit phone numbers
        if not re.match(r'^\+?\d{10,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number (10-15 digits).")

        # Uniqueness check
        if get_user_model().objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number is already in use.")

        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = get_user_model()(
            email=validated_data['email'],
            phone=validated_data['phone'],
            is_owner=validated_data['is_owner'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['id', 'user', 'rating', 'created_at', 'updated_at']

