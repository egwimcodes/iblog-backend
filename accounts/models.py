from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
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


class Followers(models.Model):
    target_user = models.ForeignKey(
        IBlogUser, on_delete=models.CASCADE, related_name='followers'  # Who is being followed
    )
    follower_user = models.ForeignKey(
        IBlogUser, on_delete=models.CASCADE, related_name='following'  # Who follows them
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # No duplicate follows
        unique_together = ('target_user', 'follower_user')

    def __str__(self):
        return f"{self.follower_user.username} follows {self.target_user.username}"
