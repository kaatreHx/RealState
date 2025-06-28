from typing import override
from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('room', 'Room'),
        ('flat', 'Flat'),
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('office', 'Office'),
        ('shop', 'Shop'),
        ('warehouse', 'Warehouse'),
        ('plot', 'Plot'),
        ('farm', 'Farm Land'),
    ]

    PROPERTY_STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
        ('inactive', 'Inactive'),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    property_status = models.CharField(max_length=20, choices=PROPERTY_STATUS_CHOICES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    kitchen = models.IntegerField()
    parking = models.IntegerField()
    area = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Owner: {self.owner.first_name} {self.owner.last_name} - Property Type: {self.property_type} - Address: {self.address}"

def upload_property_images(instance, filename):
    return f"property_images/{instance.property_id}/{filename}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_property_images)

    def __str__(self):
        return f"Image {self.property.property_id}"

class PropertyCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.property.property_id}"

class PropertyRating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
    
    def __str__(self):
        return f"{self.user.email} - {self.property.property_id} - Rating: {self.rating}"