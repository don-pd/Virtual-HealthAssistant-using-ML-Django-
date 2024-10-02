from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    # Additional fields if needed
    USER_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient','Patient'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username



class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Association with the logged-in user
    name = models.CharField(max_length=100)
    symptoms = models.TextField()
    predicted_disease = models.TextField()

    def __str__(self):
        return f"{self.name}'s Diagnosis" 