from django.urls import path, include
from .views import RentBookingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rent-booking', RentBookingViewSet, basename='rent-booking')

urlpatterns = [
    path('booking/', include(router.urls)),
]