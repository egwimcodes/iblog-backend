from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Account"])
class MyTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=["Account"])
class MyTokenRefreshView(TokenRefreshView):
    pass
