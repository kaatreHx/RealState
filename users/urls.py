from django.urls import path
from .views import RegisterView, LoginView, UserRatingViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register(r'user-rating', UserRatingViewSet, basename='user-rating')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]