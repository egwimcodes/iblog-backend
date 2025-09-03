from rest_framework import serializers
from core.account.models import IBlogUser
from core.followers.models import Followers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from core.utils import is_valid_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

# Authentication Serializer

class RegisterAccountSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "Passwords do not match."})

        if IBlogUser.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "This email is already taken."})

        validate_password(attrs["password1"])

        return attrs

    def create(self, validated_data):
        """Create and return a new user"""
        user = IBlogUser.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password1"],
        )
        return user
        
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        email = attrs.get('username_or_email')
        password = attrs.get('password')

        if email and password:
            if is_valid_email():
                try:
                    user = IBlogUser.objects.get(email=email)
                    email = user.email
                except IBlogUser.DoesNotExist:
                    raise serializers.ValidationError(
                        'No account found with this email address.',
                        code='email_not_found'
                    )
            else:
                raise serializers.ValidationError(
                    'Invalide email address',
                    code='username_not_found'
                )

            # Authenticate the user
            user = authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError(
                    'Invalid password. Please try again.',
                    code='invalid_password'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    'This account has been deactivated.',
                    code='account_inactive'
                )

            attrs['user'] = user
            return attrs

        raise serializers.ValidationError(
            'Both email and password are required.',
            code='missing_credentials'
        )


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')

        # Basic validation - you can add more checks here
        if not refresh_token:
            raise serializers.ValidationError({
                'refresh_token': 'Refresh token is required'
            })

        return attrs
    
   
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = IBlogUser.objects.get(email=email)
        except IBlogUser.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "No user found with this email."})

        # Generate token & uid
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build password reset link
        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"
        # In production, you’d use your frontend domain:
        # reset_link = f"https://yourfrontend.com/reset-password/{uid}/{token}/"

        # Send email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n\n{reset_link}",
            from_email="egwimcodes@gmail.com",
            recipient_list=[user.email],
        )

        return attrs

    
class PasswordResetDoneSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        password1 = attrs.get("new_password1")
        password2 = attrs.get("new_password2")

        if password1 != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = IBlogUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid UID"})

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {"token": "Invalid or expired token"})

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        password = self.validated_data["new_password1"]
        user.set_password(password)
        user.save()
        return user


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()
    
    
class IBlogUserSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = IBlogUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'follower_count', 'following_count', 'is_following',
                  'is_active', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_active']

    def get_follower_count(self, obj) -> int:
        return obj.followers.count()

    def get_following_count(self, obj) -> int:
        return obj.following.count()

    def get_is_following(self, obj) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Followers.objects.filter(target_user=obj, follower_user=request.user).exists()
        return False

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



class GoogleAuthResposneSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = IBlogUserSerializer()
