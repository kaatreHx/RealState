from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('test/', views.test, name='test'),
    path('login/', TemplateView.as_view(template_name='chat/login.html'), name='login'),
]