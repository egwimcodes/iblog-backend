from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# Create your models here.


class IBlogUser(AbstractUser):
    email = models.EmailField(
        unique=True, max_length=255, verbose_name="email address",)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "IBlog User"
        verbose_name_plural = "IBlog Users"
