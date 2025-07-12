from django.contrib import admin
from .models import CustomUser, CustomerVerification, UserRating

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_owner', 'is_staff', 'is_active', 'is_online', 'created_at', 'updated_at')
    list_filter = ('is_owner', 'is_staff', 'is_active', 'is_online', 'created_at', 'updated_at')
    search_fields = ('email', 'username')

@admin.register(CustomerVerification)
class CustomerVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'dob', 'gender', 'profile_image', 'address', 'city', 'country', 'postal_code', 'document_type', 'document_number', 'document_front', 'document_back', 'is_verified', 'created_at', 'updated_at')
    list_filter = ('user', 'is_verified', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'first_name', 'last_name', 'document_number')
    
@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
