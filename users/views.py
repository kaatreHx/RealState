from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from .models import UserRating, CustomUser
from .serializers import RegisterSerializer, UserRatingSerializer, LoginSerializer, CustomUserSerializer, GoogleLoginSerializer
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from google.auth.transport.requests import Request
from google.oauth2 import id_token

class RegisterView(APIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(GenericAPIView):
    serializer_class = GoogleLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get("id_token")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            userinfo = id_token.verify_oauth2_token(token, Request())

            username = userinfo.get("name")
            email = userinfo.get("email")

            user = CustomUser.objects.filter(email=email).first()
            if user: 
                return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = CustomUser.objects.create_user(email=email, username=username)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "User created successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": f"Invalid token: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

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
            user = get_user_model().objects.filter(username=id).first()
        
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
                'username': user.username,
                'is_owner': user.is_owner,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'is_online': user.is_online,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
            }
        }, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = CustomUser.objects.all()
    http_method_names = ['get', 'put', 'delete']
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

class UserRatingViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]