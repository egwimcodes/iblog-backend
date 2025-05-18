from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from .models import IBlogUser, BlogPost, Category
from .serializers import IBlogUserSerializer, CreateBlogSerializer, BlogPostSerializer, CategorySerializer
# Create your views here.
# GCBV


class AllIblogUser(ListAPIView):
    serializer_class = IBlogUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IBlogUser.objects.all()


class CreateIBlogUserGCBV(ListCreateAPIView):
    serializer_class = IBlogUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IBlogUser.objects.all()

    def create(self, request, *args, **kwargs):
        get_username = request.data.get("username")
        user_exist = IBlogUser.objects.filter(
            username__iexact=get_username).exists()

        if user_exist:
            return Response({"error": "User is taken"}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        return Response({"message": "User Successfully created!", "user": response.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class RegsiterIBlogUserView(RetrieveUpdateDestroyAPIView):
    pass
#     serializer_class =
#     def ge


class CreateBlogView(ListCreateAPIView):
    serializer_class = CreateBlogSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.all()
