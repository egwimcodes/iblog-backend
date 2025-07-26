from django.urls import path
from .views.user_registration_login_logout_view import CreateListIBlogUsersGCBV, IBlogUserRetrieveUpdateDestroyView, IBlogUserLogOut
from .views.auth.google_registration_login import GoogleLoginApiView
from .views.followers_views import FollowUserView, UnfollowUserView, FollowersListView, FollowingListView

from .views.auth.password_reset_view import (
    PasswordResetConfirmView,
    PasswordResetRequestView,
)
from .views.auth.token_handlers import (
    MyTokenObtainPairView, MyTokenRefreshView
)
from .views.auth.password_change_views import PasswordChangeView

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("google/initialize_google_login/", GoogleLoginApiView.as_view(), name="initialize_google_login"), path(
        "google/finalize_google_login/", GoogleLoginApiView.as_view(), name="finalize_google_login"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path("register/", CreateListIBlogUsersGCBV.as_view(), name="register"),
    path("me/", IBlogUserRetrieveUpdateDestroyView.as_view(), name="user"),
    path("me/logout/", IBlogUserLogOut.as_view(), name="logout-user"),
    
    
    # Followers
    path('me/follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('me/unfollow/<int:user_id>/',
         UnfollowUserView.as_view(), name='unfollow-user'),
    path('me/followers/<int:user_id>/',
         FollowersListView.as_view(), name='followers-list'),
    path('me/following/<int:user_id>/',
         FollowingListView.as_view(), name='following-list'),
]
