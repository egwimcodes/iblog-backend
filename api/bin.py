from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from .models import IBlogUser, BlogPost, Category
from .Blogs.serializers import IBlogUserSerializer, BlogPostSerializer, CategorySerializer
# Create your views here.
# FBV


@api_view(['POST'])
def createIBlogUserFBV(request):
    user_exists = IBlogUser.objects.filter(
        username__iexact=request.data.get('username')).exists()

    serialized_user = IBlogUserSerializer(data=request.data)
    if not user_exists and serialized_user.is_valid():
        serialized_user.save()
        return Response("User Successfully created!", status=status.HTTP_201_CREATED)

    if user_exists:
        return Response("Username taken", status=status.HTTP_400_BAD_REQUEST)

    return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

# CBV testing init ....
