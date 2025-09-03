from django.db import models
from core.account.models import IBlogUser
# Create your models here.


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
