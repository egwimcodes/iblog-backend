from .serializers import BlogPostSerializer
from .models import BlogPost
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from .models import IBlogUser, BlogPost, Category
from .serializers import IBlogUserSerializer, CreateBlogSerializer, BlogPostSerializer, CategorySerializer
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


class RetrieveUpdateDestroyIBlogUserView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "message": "Blog post retrieved successfully ✅",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # For PATCH support
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Blog post updated successfully ✏️",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Blog post deleted successfully 🗑️"
        }, status=status.HTTP_204_NO_CONTENT)



class CreateBlogView(ListCreateAPIView):
    serializer_class = CreateBlogSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.all()

