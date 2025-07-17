from rest_framework import serializers
from .models import RentBooking
from users.serializers import CustomUserSerializer
from property.serializers import PropertySerializer

class RentBookingSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()
    property = PropertySerializer()

    class Meta:
        model = RentBooking
        fields = '__all__'

