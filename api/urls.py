from django.urls import path
 
from .views import BlogListCreateAPIView, BlogViewRetrieveUpdateDestroy

urlpatterns = [
   
    path("create-blog/", BlogListCreateAPIView.as_view(), name='create-blog'
         ),
    path("blogs/", BlogListCreateAPIView.as_view(), name='all-blog'
         ),
    path("blog/", BlogViewRetrieveUpdateDestroy.as_view(),
         name="get-blog"),
    #     path("blogs/<int:pk>/",IBlogUserRetrieveUpdateDestroyView.as_view(), name="get-rudibusv" ),
    #     path("blogs/<int:pk>/",
    #          IBlogUserRetrieveUpdateDestroyView.as_view(), name="update-rudibusv"),
    #     path("blogs/<int:pk>/",
    #          IBlogUserRetrieveUpdateDestroyView.as_view(), name="delete-rudibusv"),

]
