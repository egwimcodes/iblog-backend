from django.urls import path
from .views import  CreateIBlogUserGCBV, AllIblogUser, CreateBlogView

urlpatterns = [
    path("register/", CreateIBlogUserGCBV.as_view(), name='register'),
    path("users/", AllIblogUser.as_view(), name="all_user"),
    path("blogs/", CreateBlogView.as_view(), name='blogs')
]
