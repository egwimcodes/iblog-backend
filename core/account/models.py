from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class IBlogUser(AbstractUser):
    email = models.EmailField(
        unique=True, max_length=255, verbose_name="email address",)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "IBlog User"
        verbose_name_plural = "IBlog Users"


