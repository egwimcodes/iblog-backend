from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from .models import IBlogUser, BlogPost,PostCategory

# Create your models here.
class IBlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IBlogUser
        fields = ['username','first_name', 'last_name','email','is_active']
        extra_kwargs = {'password':{'write_only':True}}
        read_only_fields = ['is_active']
        
        
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title']

class PostCategorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = PostCategory
        fields = ['category']
        