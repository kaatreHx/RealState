from django.db import models

class RentBooking(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.property.property_type} - {self.status}"

    
    