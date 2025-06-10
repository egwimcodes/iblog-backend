from rest_framework import serializers
from ...models import IBlogUser
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator




class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = IBlogUser.objects.get(email=value)
        except IBlogUser.DoesNotExist:
            raise serializers.ValidationError(
                "No user with this email address exists.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            self.user = IBlogUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, IBlogUser.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid user ID"})

        if not PasswordResetTokenGenerator().check_token(self.user, data['token']):
            raise serializers.ValidationError(
                {"token": "Invalid or expired token"})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords don't match"})

        return data
