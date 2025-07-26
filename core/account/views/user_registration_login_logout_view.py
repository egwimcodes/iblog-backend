from core.account.models import IBlogUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from ..serializers import IBlogUserSerializer  
from drf_spectacular.utils import extend_schema



# CREATES A USER
@extend_schema(tags=["Account"])
class CreateListIBlogUsersGCBV(ListCreateAPIView):
    serializer_class = IBlogUserSerializer

    def create(self, request, *args, **kwargs):
        get_username = request.data.get("username")
        get_email = request.data.get("email")

        username_exist = IBlogUser.objects.filter(
            username__iexact=get_username).exists()
        email_exist = IBlogUser.objects.filter(
            email__iexact=get_email).exists()

        if username_exist:
            return Response({"error": "User is taken"}, status=status.HTTP_400_BAD_REQUEST)
        if email_exist:
            return Response({"error": "email exist"}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        return Response({"message": "User Successfully created!", "user": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        patial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, patial=patial)

        serializer.is_valid(raise_exception=True)
        self.perform_save(serializer)

    def perform_create(self, serializer):
        serializer.save()


# RETRIVE UPDATES AND DELETES A USER
@extend_schema(tags=["Account"])
class IBlogUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = IBlogUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.request.query_params.get("username")

        if username:
            return IBlogUser.objects.filter(username__iexact=username)
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)

        return Response({
            "message": "User  updated successfully ✏️",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "User deleted successfully 🗑️"
        }, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Account"])
class IBlogUserLogOut(APIView):
    permission_classes = [IsAuthenticated]
     
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token is None:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
