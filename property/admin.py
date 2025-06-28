from django.contrib import admin
from .models import Property, PropertyImage, PropertyCart, PropertyRating

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_type', 'property_status', 'address', 'city', 'state', 'price', 'bedrooms', 'bathrooms', 'kitchen', 'parking', 'area', 'description', 'created_at', 'updated_at')
    list_filter = ('property_type', 'property_status', 'price')
    search_fields = ('address', 'city', 'state')
    ordering = ('-created_at',)

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'image')
    list_filter = ('property',)
    search_fields = ('property',)

@admin.register(PropertyCart)
class PropertyCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'added_at')
    list_filter = ('user', 'property')
    search_fields = ('user', 'property')
    ordering = ('-added_at',)

@admin.register(PropertyRating)
class PropertyRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'rating', 'created_at')
    list_filter = ('user', 'property')
    search_fields = ('user', 'property')
    ordering = ('-created_at',)