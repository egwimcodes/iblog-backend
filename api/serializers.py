from django.db import models
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import  BlogPost, Category


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content',
                  'author', 'featured_img', 'published_date']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category']


