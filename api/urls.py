from django.urls import path
from .views import CreateIBlogUserGCBV, AllIblogUser, CreateBlogView, RetrieveUpdateDestroyIBlogUserView

urlpatterns = [
    path("register/", CreateIBlogUserGCBV.as_view(), name='register'),
    path("allusers/", AllIblogUser.as_view(), name="all_user"),
    path("blogs/", CreateBlogView.as_view(), name='blogs'),
    path("blogs/<int:pk>/",RetrieveUpdateDestroyIBlogUserView.as_view(), name="get-rudibusv" ),
    path("blogs/<int:pk>/",
         RetrieveUpdateDestroyIBlogUserView.as_view(), name="update-rudibusv"),
    path("blogs/<int:pk>/",
         RetrieveUpdateDestroyIBlogUserView.as_view(), name="delete-rudibusv"),
    
]
