from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from .models import IBlogUser, BlogPost, Category
from rest_framework_simplejwt.tokens import RefreshToken


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id','title','slug','content', 'author']
        
# Create your models here.
class IBlogUserSerializer(serializers.ModelSerializer):
    blogs = BlogPostSerializer(many=True)
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()
    
    class Meta:
        model = IBlogUser
        fields = ['id','username','first_name', 'last_name','email','is_active', 'blogs','access', 'refresh']
        extra_kwargs = {'password':{'write_only':True}}
        read_only_fields = ['is_active']

    def get_access(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)

    def get_refresh(self, user):
        token = RefreshToken.for_user(user)
        return str(token)

        


class CategorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Category
        fields = ['category']
        
        

class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title','content','author','featured_img']