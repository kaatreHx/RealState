from rest_framework import generics
from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import Property, PropertyImage, PropertyCart, PropertyRating
from users.models import CustomUser
from .serializers import PropertySerializer, PropertyImageSerializer, PropertyCartSerializer, PropertyRatingSerializer
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'delete']

class ListProperty(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property_type', 'property_status', 'price']
    search_fields = ['address', 'city', 'state']
    ordering_fields = ['price', 'created_at']

class PropertyCartViewSet(viewsets.ModelViewSet):
    queryset = PropertyCart.objects.all()
    serializer_class = PropertyCartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class PropertyRatingViewSet(viewsets.ModelViewSet):
    queryset = PropertyRating.objects.all()
    serializer_class = PropertyRatingSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
