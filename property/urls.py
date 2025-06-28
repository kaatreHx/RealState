from django.urls import path, include
from .views import PropertyViewSet, PropertyImageViewSet, ListProperty, PropertyCartViewSet, PropertyRatingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'properties-image', PropertyImageViewSet, basename='property-image')
router.register(r'cart', PropertyCartViewSet, basename='property-cart')
router.register(r'reviews', PropertyRatingViewSet, basename='property-rating')

urlpatterns = [
    path('property/', include(router.urls)),
    path('property/list/', ListProperty.as_view(), name='property-list'),
]