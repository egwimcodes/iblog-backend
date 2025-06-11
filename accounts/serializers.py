from rest_framework import serializers 
from post.serializers import PostSerializer
from .models import IBlogUser, Followers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password



class IBlogUserSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    posts = PostSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = IBlogUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'follower_count', 'following_count', 'is_following',
                  'is_active', 'posts', 'password', 'password2', 'access', 'refresh']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_active']

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Followers.objects.filter(target_user=obj, follower_user=request.user).exists()
        return False
    
    def get_access(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)

    def get_refresh(self, user):
        token = RefreshToken.for_user(user)
        return str(token)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password or password2:
            if password != password2:
                raise serializers.ValidationError(
                    {"password": "Passwords do not match."})
            validate_password(password)

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = IBlogUser.objects.create_user(**validated_data)
        return user


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ['id', 'target_user', 'follower_user', 'followed_at']
        read_only_fields = ['followed_at']
