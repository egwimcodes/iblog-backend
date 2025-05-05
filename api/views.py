from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from .models import IBlogUser, BlogPost, PostCategory
from .serializers import IBlogUserSerializer, BlogPostSerializer, PostCategorySerializer
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

# CBV


class CreateIBlogUserCBV():
    permission_classes = []

    def pos(self, request): 
        get_username = request.data.get("username")
        user_exist = IBlogUser.objects.filter(
            username__iexact=get_username).exists()
        serialized_user = IBlogUserSerializer(data=request.data)

        if not user_exist and serialized_user.is_valid():
            serialized_user.save()
            return Response("User Successfully created!", status=status.HTTP_201_CREATED)

        if user_exist:
            return Response("Username taken", status=status.HTTP_400_BAD_REQUEST)

        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

# GCBV


class CreateIBlogUserGCBV(CreateAPIView):
    serializer_class = IBlogUserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
         get_username = request.data.get("username")
         user_exist = IBlogUser.objects.filter(
             username__iexact=get_username).exists()

         if user_exist:
            return Response({"error": "User is taken"}, status=status.HTTP_400_BAD_REQUEST)

         response = super().create(request, *args, **kwargs)
         return Response({"message":"User Successfully created!","user": response.data}, status=status.HTTP_201_CREATED)
    
    
    def perform_create(self, serializer):
        serializer.save()
    
class AllIblogUser(ListAPIView):
    serializer_class = IBlogUserSerializer
    permission_classes = []
    
    def get_queryset(self):
        return IBlogUser.objects.all()
    
# class RegsiterIBlogUserView(RetrieveUpdateDestroyAPIView):
#     serializer_class =
#     def ge
