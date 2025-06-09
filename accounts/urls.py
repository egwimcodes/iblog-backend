from django.urls import path
from .views import GoogleLoginApiView
from django.contrib.auth import views as auth_views
from .views import CreateListBlogUsersGCBV, IBlogUserRetrieveUpdateDestroyView, PasswordResetConfirmView, PasswordResetRequestView

urlpatterns = [
    path('google/login/', GoogleLoginApiView.as_view(), name="google_login_api"),
    path('password-reset/', PasswordResetRequestView.as_view(),
         name='password_reset'),
    path('password-reset/confirm/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("register/", CreateListBlogUsersGCBV.as_view(), name='register'),
    path("user/", IBlogUserRetrieveUpdateDestroyView.as_view(), name="user"),
]

#