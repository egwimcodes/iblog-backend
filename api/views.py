from .serializers import BlogPostSerializer
from .models import BlogPost
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import BlogPost
from .serializers import BlogPostSerializer

            

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




