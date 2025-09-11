from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class IBlogUser(AbstractUser):
    username = models.CharField( max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True, max_length=255, verbose_name="email address")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"   # 👈 This tells Django to use email for authentication
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "IBlog User"
        verbose_name_plural = "IBlog Users"
