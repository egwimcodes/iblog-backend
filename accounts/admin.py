from django.contrib import admin
from .models import IBlogUser, Followers
from unfold.admin import ModelAdmin
# Register your models here.


@admin.register(IBlogUser)
class IBlogUserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff']


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ('target_user', 'follower_user', 'followed_at')
    search_fields = ('target_user__username', 'follower_user__username')
