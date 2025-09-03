from django.urls import path

from core.followers.views import FollowUserView, FollowersListView, FollowingListView, UnfollowUserView

urlpatterns = [
    # Followers
    path('me/follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('me/unfollow/<int:user_id>/',
         UnfollowUserView.as_view(), name='unfollow-user'),
    path('me/followers/<int:user_id>/',
         FollowersListView.as_view(), name='followers-list'),
    path('me/following/<int:user_id>/',
         FollowingListView.as_view(), name='following-list'),
]