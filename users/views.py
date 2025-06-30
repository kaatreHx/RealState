from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from .models import UserRating
from .serializers import RegisterSerializer, UserRatingSerializer, LoginSerializer
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

class RegisterView(APIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = LoginSerializer
    
    def post(self, request):
        id = request.data.get('id')
        password = request.data.get('password')

        if not id or not password:
            return Response({
                'error': 'Both id and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_model().objects.filter(email=id).first()
        if not user:
            user = get_user_model().objects.filter(phone=id).first()
        
        if not user or not user.check_password(password):
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'phone': user.phone,
                'is_owner': user.is_owner,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'is_online': user.is_online,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
            }
        }, status=status.HTTP_200_OK)

class UserRatingViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer