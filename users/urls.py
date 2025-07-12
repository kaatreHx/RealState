from django.urls import path
from .views import RegisterView, LoginView, UserRatingViewSet, UserViewSet, GoogleLoginView
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register(r'user-rating', UserRatingViewSet, basename='user-rating')
router.register(r'users-data', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('', include(router.urls)),
]