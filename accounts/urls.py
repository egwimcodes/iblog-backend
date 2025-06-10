from django.urls import path
from .views.user_registration_login_logout_view import CreateListIBlogUsersGCBV, IBlogUserRetrieveUpdateDestroyView, IBlogUserLogOut
from .views.auth.google_registration_login import GoogleLoginApiView
from .views.auth.password_reset_view import (
    PasswordResetConfirmView,
    PasswordResetRequestView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google/login/", GoogleLoginApiView.as_view(), name="google_login_api"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("register/", CreateListIBlogUsersGCBV.as_view(), name="register"),
    path("user/", IBlogUserRetrieveUpdateDestroyView.as_view(), name="user"),
    path("logout/", IBlogUserLogOut.as_view(), name="logout-user"),
]
