from django.urls import path
 
from .views import GetJWTView, CreateListBlogUsersGCBV, IBlogUserRetrieveUpdateDestroyView, BlogListCreateAPIView, BlogViewRetrieveUpdateDestroy

urlpatterns = [
    path("register/", CreateListBlogUsersGCBV.as_view(), name='register'),
    path("user/", IBlogUserRetrieveUpdateDestroyView.as_view(), name="user"),
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
