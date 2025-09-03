# followers/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from core.account.models import IBlogUser  
from core.followers.models import Followers
from drf_spectacular.utils import extend_schema

from core.followers.serializers import FollowerSerializer


@extend_schema(tags=["Followers"])
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(IBlogUser, id=user_id)
        if request.user == target_user:
            return Response({"detail": "You can't follow yourself."}, status=400)

        follower_obj, created = Followers.objects.get_or_create(
            target_user=target_user, follower_user=request.user)

        if not created:
            return Response({"detail": "You already follow this user."}, status=400)

        serializer = FollowerSerializer(follower_obj)
        return Response(serializer.data, status=201)


@extend_schema(tags=["Followers"])
class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        target_user = get_object_or_404(IBlogUser, id=user_id)
        try:
            follow_obj = Followers.objects.get(
                target_user=target_user, follower_user=request.user)
            follow_obj.delete()
            return Response({"detail": "Unfollowed successfully."}, status=204)
        except Followers.DoesNotExist:
            return Response({"detail": "You do not follow this user."}, status=400)


@extend_schema(tags=["Followers"])
class FollowersListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(IBlogUser, id=user_id)
        followers = user.followers.all()
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Followers"])
class FollowingListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(IBlogUser, id=user_id)
        following = user.following.all()
        serializer = FollowerSerializer(following, many=True)
        return Response(serializer.data)
