from django.urls import path
from .views import createIBlogUserFBV, CreateIBlogUserCBV, CreateIBlogUserGCBV, AllIblogUser
urlpatterns = [
    path("users/", AllIblogUser.as_view(), name="all user"),
    path("createuserfbv/", createIBlogUserFBV, name='createuserfbv'),
    path("createusercbv/", CreateIBlogUserCBV, name='createusercbv'),
    path("createusergcbv/", CreateIBlogUserGCBV.as_view(), name='createusergcbv')
]
