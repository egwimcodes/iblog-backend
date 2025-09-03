from rest_framework import serializers
from core.followers.models import Followers

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ['id', 'target_user', 'follower_user', 'followed_at']
        read_only_fields = ['followed_at']
