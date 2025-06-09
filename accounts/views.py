from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from rest_framework.views import APIView
from .serializers import GoogleAuthSerializer
from .services.google_oauth import verify_google_token
from accounts.models import IBlogUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from .serializers import IBlogUserSerializer  
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

# CREATES A USER FROM GOOGLE LOGIN
class GoogleLoginApiView(APIView):
    """
    Receives Google ID token from frontend, verifies it, and logs in/creates user.
    Returns: Auth token (e.g., JWT or DRF Token)
    """
    
    def post(self, request):
        if not request.data.get("token"):
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            user_info = verify_google_token(token)
        except ValueError as e:
            return e
        
        print(f"### Res {str(user_info)}")
        
        email = user_info.get("email")
        name = user_info.get("name", "")
        user, created = IBlogUser.objects.get_or_create(
            email=email, defaults={"username": email.split("@")[0], "first_name": name})
        print(f"### User Creates {str(user)} - {created}")
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "name": user.first_name,
            }
        })


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        print(str(serializer))
        if serializer.is_valid():
            user = serializer.user
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"{request.build_absolute_uri('/')}api/accounts/password-reset/confirm/?uid={uid}&token={token}"

            # Email context
            context = {
                'reset_url': reset_url,
                'site_name': settings.SITE_NAME,  # Add to your settings.py
                'user': user,
            }

            # Render HTML and text versions
            email_html_message = render_to_string(
                'emails/password_reset_email.html',
                context
            )
            email_plaintext_message = render_to_string(
                'emails/password_reset_email.txt',
                context
            )

            # Create email
            msg = EmailMultiAlternatives(
                "Password Reset Request",
                email_plaintext_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()

            return Response(
                {"detail": "Password reset link has been sent to your email"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {"detail": "Password has been reset successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CREATES A USER
class CreateListBlogUsersGCBV(ListCreateAPIView):
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
