from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import IBlogUser, BlogPost,PostCategory
from .serializers import IBlogUserSerializer, BlogPostSerializer, PostCategorySerializer
# Create your views here.

# GCBV
class RegsiterIBlogUserView(ListCreateAPIView):
    queryset = IBlogUser.objects.all()
    serializer_class = IBlogUserSerializer
    
    
    
    
    
# class RegsiterIBlogUserView(RetrieveUpdateDestroyAPIView):
#     serializer_class = 
#     def ge