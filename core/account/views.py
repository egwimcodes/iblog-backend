from tokenize import TokenError
import jwt
from rest_framework import decorators, authentication, viewsets
from rest_framework.response import Response
from rest_framework import status
from core.account import models
from rest_framework import mixins
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from core.account.serializers import (
    AuthResponseSerializer,
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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

@extend_schema(tags=["Auth"])
class AuthView(viewsets.GenericViewSet):
    @extend_schema(
        description="""
        User login endpoint
        POST /api/auth/register/
        """,
        request=RegisterAccountSerializer,
        responses={
            200: OpenApiResponse(response=AuthResponseSerializer, description="User registered successfully"),
            400: OpenApiResponse(description="Bad request - validation error"),
        }

    )
    @decorators.action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        
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
        else:
            return Response({
                "message": serializer.errors,}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="""
        User login endpoint
        POST /api/auth/login/
        """,
        request=LoginSerializer,
        responses={200: OpenApiResponse(
            AuthResponseSerializer, description="User Credentials"), 400: OpenApiResponse(description="Bad request")},
    )
    @decorators.action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user=user)

        return Response(
            {
                # return serialized user info
                "user": IBlogUserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User logged in successfully",
            },
            status=status.HTTP_200_OK,
        )


    @extend_schema(
        description="""
        User login endpoint
        POST /api/auth/logout/
        """,
        request=LogoutSerializer,
        responses={
            200: OpenApiResponse(
                response=dict,  # or create a proper response serializer
                description="Logout successful",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Successfully logged out",
                        },
                        status_codes=["200"]
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Error Example",
                        value={"error": "Invalid token"},
                        status_codes=["400"]
                    )
                ]
            ),
        },
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
        
        POST /api/auth/google_login/
        """,
        request=GoogleAuthSerializer,
        responses={200: OpenApiResponse(
            AuthResponseSerializer, description="Returns user data"), 400: OpenApiResponse(description="Bad request")},
    )
    @decorators.action(detail=False, methods=["post"], url_path="google_login")
    def google_login(self, request):
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
            print("✅ Google user info:", user_info)
        except ValueError as e:
            return Response(
                {"error": str(e)},
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
            return Response({"message": "Password reset link has being sent to you email"}, status=status.HTTP_200_OK)

    @extend_schema(
        description="""
        Google login endpoint
        POST /api/auth/google/password-reset-done/
        """,
        request=PasswordResetDoneSerializer,
        responses={
            200: OpenApiResponse(
                response=PasswordResetDoneSerializer,  # or create a proper response serializer
                description="New Password set",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Password reset successful",
                        },
                        status_codes=["200"]
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Error Example",
                        value={"error": "Invalid token"},
                        status_codes=["400"]
                    )
                ]
            ),
        },
    )
    @decorators.action(detail=False, methods=["post"], url_path="password-reset-done")
    def password_reset_done(self, request):
        serializer = PasswordResetDoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Account"])
class UserAccountManagementView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """
    Account management endpoints.
    - Regular users: can view & update their own profile (`/me/`).
    - Admins: can list, retrieve, update or delete any user.
    """

    queryset = models.IBlogUser.objects.all()
    serializer_class = IBlogUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get current user",
        description="Returns the profile of the logged-in user.",
        responses={200: IBlogUserSerializer,
                   401: OpenApiResponse(description="Unauthorized")},
    )
    @decorators.action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Update current user",
        description="Update the profile of the logged-in user. Supports partial updates (PATCH).",
        request=IBlogUserSerializer,
        responses={200: IBlogUserSerializer, 400: OpenApiResponse(
            description="Validation Error")},
    )
    @decorators.action(detail=False, methods=["put", "patch"], url_path="me")
    def update_me(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        """
        Admins can manage all users. Normal users only access /me/.
        """
        if self.action in ["list", "retrieve", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def handle_exception(self, exc):
        """Return cleaner error messages for frontend developers"""
        response = super().handle_exception(exc)
        if response is not None:
            return Response(
                {
                    "error": True,
                    "message": response.data.get("detail", "Something went wrong"),
                    "code": getattr(exc, "default_code", "error"),
                },
                status=response.status_code,
            )
        return response
