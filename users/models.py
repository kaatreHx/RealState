from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_owner', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

def user_profile_image_path(instance, filename):
    return f'profile_images/user_{instance.id}/{filename}'

def user_kyc_document_path(instance, filename):
    return f'kyc_documents/user_{instance.user.id}/{filename}'

class CustomerVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    #User info
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    dob = models.DateField()

    gender_choice = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    gender = models.CharField(max_length=10, choices=gender_choice)
    profile_image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    
    # Address info
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    # Identity documents
    document_type = models.CharField(max_length=50, choices=[('nid', 'National ID'), ('passport', 'Passport'), ('license', 'Driver License')])
    document_number = models.CharField(max_length=100, unique=True)
    document_front = models.ImageField(upload_to=user_kyc_document_path, blank=True, null=True)
    document_back = models.ImageField(upload_to=user_kyc_document_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UserRating(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"