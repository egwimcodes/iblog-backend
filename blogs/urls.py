from django.urls import path
from .views import BlogListCreateAPIView, BlogViewRetrieveUpdateDestroy
urlpatterns = [
    path("create-blog/", BlogListCreateAPIView.as_view(), name="create-blog"),
    path("", BlogViewRetrieveUpdateDestroy.as_view(), name="get-blog"),
    path("blogs/", BlogListCreateAPIView.as_view(), name="all-blog"),
]
