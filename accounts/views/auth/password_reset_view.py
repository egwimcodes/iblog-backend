from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from django.template.loader import render_to_string


class PasswordResetRequestView(APIView):
    """
    Send POST Request to recieve a password reset link
    
    """
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"{request.build_absolute_uri('/')}api/accounts/password-reset/confirm/?uid={uid}&token={token}"

            # Email context
            context = {
                'password_reset_url': reset_url,
                'site_name': settings.SITE_NAME,  # Add to your settings.py
                'user': user,
            }

            # Render HTML and text versions
            email_html_message = render_to_string(
                'account/email/password_reset_key_message.html',
                context
            )
            email_plaintext_message = render_to_string(
                'account/email/password_reset_email.txt',
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
