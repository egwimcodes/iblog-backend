from tokenize import TokenError
from rest_framework import decorators, authentication, viewsets
from rest_framework.response import Response
from rest_framework import status
from core.account import models
from rest_framework import mixins
from drf_spectacular.utils import OpenApiResponse
from core.account.serializers import (
    GoogleAuthSerializer,
    IBlogUserSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetDoneSerializer,
    PasswordResetSerializer,
    RegisterAccountSerializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from core.account.services.google_oauth import verify_google_token


@extend_schema(tags=["Auth"])
class AuthView(viewsets.GenericViewSet):
    @extend_schema(
        description="""
        User login endpoint
        POST /api/auth/register/
        """,
        request=RegisterAccountSerializer,
        responses={
            200: OpenApiResponse(response=RegisterAccountSerializer, description="User registered successfully"),
            400: OpenApiResponse(description="Bad request - validation error"),
        }

    )
    @decorators.action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):
        serializer = RegisterAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user=user)
            return Response(
                {
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )

    @extend_schema(
        description="""
        User login endpoint
        POST /api/auth/login/
        """,
        request=LoginSerializer,
        responses={200, LoginSerializer},
    )
    @decorators.action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user=user)

            return Response(
                {
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "User logged in successfully",
                },
                status=status.HTTP_201_CREATED,
            )

    @extend_schema(
        description="""
        User login endpoint
        POST /api/auth/logout/
        """,
        request=LogoutSerializer,
        responses={200, LogoutSerializer},
    )
    @decorators.action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        """
        JWT Logout endpoint
        POST /auth/logout/
        Requires: {"refresh_token": "your_refresh_token"}
        """
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            refresh_token = serializer.validated_data["refresh_token"]

            try:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response(
                    {
                        "message": "Successfully logged out",
                        "details": "Refresh token has been blacklisted",
                    },
                    status=status.HTTP_200_OK,
                )

            except TokenError as e:
                return Response(
                    {"error": "Invalid or expired token", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    {"error": "Logout failed", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="""
        Google login endpoint
        POST /api/auth/google/google_login/
        """,
        request=IBlogUserSerializer,
        responses={200, IBlogUserSerializer},
    )
    @decorators.action(detail=False, methods=["post"], url_path="google_login")
    def google_login(self, request, *args, **kwargs):
        if not request.data.get("token"):
            return Response(
                {"error": "Token not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]

        try:
            user_info = verify_google_token(token)
            print("Data", str(user_info))
        except ValueError as e:
            return Response(
                {"error": f"Invalid Google token: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = user_info.get("email", "")
        name = user_info.get("name", "")
        user, created = models.IBlogUser.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": name
            }
        )
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": IBlogUserSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        description="""
        Google login endpoint
        POST /api/auth/google/password-reset/
        """,
        request=PasswordResetSerializer,
        responses={200, PasswordResetSerializer},
    )
    @decorators.action(detail=False, methods=["post"], url_path="password-reset")
    def password_reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)

    @extend_schema(
        description="""
        Google login endpoint
        POST /api/auth/google/password-reset-done/
        """,
        request=PasswordResetDoneSerializer,
        responses={200, PasswordResetDoneSerializer},
    )
    @decorators.action(detail=False, methods=["post"], url_path="password-reset-done")
    def password_reset_done(self, request):
        serializer = PasswordResetDoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Account"])
class UserAccountManagementView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = models.IBlogUser.objects.all()
    serializer_class = IBlogUserSerializer
