from typing import override
from rest_framework.viewsets import ModelViewSet
from .models import RentBooking
from .serializers import RentBookingSerializer
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated

class RentBookingViewSet(ModelViewSet):
    queryset = RentBooking.objects.all()
    serializer_class = RentBookingSerializer
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    
        