from django.urls import path
from .views import  CreateIBlogUserGCBV, AllIblogUser

urlpatterns = [
    path("users/", AllIblogUser.as_view(), name="all user"),
    path("register/", CreateIBlogUserGCBV.as_view(), name='register')
]
