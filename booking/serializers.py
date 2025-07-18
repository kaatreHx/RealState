from rest_framework import serializers
from .models import RentBooking
from users.models import CustomUser
from property.models import Property

class RentBookingSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = RentBooking
        fields = '__all__'
        read_only_fields = ('status', 'user')
    
    def create(self, validated_data):
        user = self.context['request'].user
        return RentBooking.objects.create(user=user, **validated_data)

