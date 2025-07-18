from rest_framework import serializers
from .models import Property, PropertyImage, PropertyCart, PropertyRating
from users.models import CustomUser, CustomerVerification

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate(self, data):
        if data['price'] < 0:
            raise serializers.ValidationError("Price cannot be negative")
        if data['bedrooms'] < 0:
            raise serializers.ValidationError("Bedrooms cannot be negative")
        if data['bathrooms'] < 0:
            raise serializers.ValidationError("Bathrooms cannot be negative")
        if data['kitchen'] < 0:
            raise serializers.ValidationError("Kitchen cannot be negative")
        if data['parking'] < 0:
            raise serializers.ValidationError("Parking cannot be negative")
        if data['area'] < 0:
            raise serializers.ValidationError("Area cannot be negative")
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        info = CustomUser.objects.filter(id = user.id).first()
        check = info.is_owner
        check_verification = info.is_verified
        if not check:
            raise serializers.ValidationError("Not permission to create property")
        if not check_verification:
            raise serializers.ValidationError("Not verified")
        
        return Property.objects.create(owner=user, **validated_data)
    
class PropertyCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCart
        fields = '__all__'

class PropertyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyRating
        fields = '__all__'
