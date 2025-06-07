from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from .models import IBlogUser, BlogPost, Category
from rest_framework_simplejwt.tokens import RefreshToken


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content',
                  'author', 'featured_img', 'published_date']

# Create your models here.


class IBlogUserSerializer(serializers.ModelSerializer):
    blogs = BlogPostSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = IBlogUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'is_active', 'blogs', 'password', 'password2', 'access', 'refresh']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_active']

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
                raise serializers.ValidationError({"password": "Passwords do not match."})
            validate_password(password)

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = IBlogUser.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category']


