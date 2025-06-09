from rest_framework import serializers 
from api.serializers import BlogPostSerializer
from .models import IBlogUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
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




class IBlogUserSerializer(serializers.ModelSerializer):
    blogs = BlogPostSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = IBlogUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'is_active', 'blogs', 'password', 'password2', 'access', 'refresh']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_active']

    def get_access(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)

    def get_refresh(self, user):
        token = RefreshToken.for_user(user)
        return str(token)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password or password2:
            if password != password2:
                raise serializers.ValidationError(
                    {"password": "Passwords do not match."})
            validate_password(password)

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = IBlogUser.objects.create_user(**validated_data)
        return user
