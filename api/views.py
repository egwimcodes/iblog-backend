from .serializers import BlogPostSerializer
from .models import BlogPost
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from .models import IBlogUser, BlogPost, Category
from .serializers import IBlogUserSerializer, BlogPostSerializer, CategorySerializer
from rest_framework_simplejwt.tokens import RefreshToken



# AUTHENTICATION VIEWS HERE
# GET JWT FOR GOOGLE LOGIN
class GetJWTView(ListAPIView):
    
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error":"User Must login first"})
        refresh = RefreshToken.for_user(self.request.user)
        return Response({
            "refresh": str(refresh),
            "access":str(refresh.access_token)
        })
            
            
# CREATES A USER
class CreateListBlogUsersGCBV(ListCreateAPIView):
    serializer_class = IBlogUserSerializer

    def create(self, request, *args, **kwargs):
        get_username = request.data.get("username")
        get_email = request.data.get("email")

        username_exist = IBlogUser.objects.filter(
            username__iexact=get_username).exists()
        email_exist = IBlogUser.objects.filter(
            email__iexact=get_email).exists()

        if username_exist:
            return Response({"error": "User is taken"}, status=status.HTTP_400_BAD_REQUEST)
        if email_exist:
            return Response({"error": "email exist"}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        return Response({"message": "User Successfully created!", "user": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        patial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, patial=patial)

        serializer.is_valid(raise_exception=True)
        self.perform_save(serializer)

    def perform_create(self, serializer):
        serializer.save()


# RETRIVE UPDATES AND DELETES A USER
class IBlogUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = IBlogUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.request.query_params.get("username")
        
        if username:
            return IBlogUser.objects.filter(username__iexact=username)
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        
        return Response({
                    "message": "User  updated successfully ✏️",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
              "message": "User deleted successfully 🗑️"
            }, status=status.HTTP_204_NO_CONTENT)


# CREATES A BLOG
class BlogListCreateAPIView(ListCreateAPIView):
    serializer_class = BlogPostSerializer
    permission_classes= [IsAuthenticated]
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)


# RETRIVE UPDATES AND DELETES A BLOG
class BlogViewRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = BlogPost
    # lookup_field = "id"
    
    def get_object(self):
        id = self.request.query_params.get("id")
        return get_object_or_404(BlogPost, id=id)

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




