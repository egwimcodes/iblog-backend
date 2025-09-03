from django.contrib import admin
from core.followers.models import Followers
# Register your models here.


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ('target_user', 'follower_user', 'followed_at')
    search_fields = ('target_user__username', 'follower_user__username')