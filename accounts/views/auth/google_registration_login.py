from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ...services.google_oauth import verify_google_token
from .serializers import GoogleAuthSerializer
from ...models import IBlogUser
from rest_framework_simplejwt.tokens import RefreshToken


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
        refresh = RefreshToken.for_user(user)
        print(f"### Users Token {str(refresh)} - {str(refresh.access_token)}")

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "name": user.first_name,
            }
        })
