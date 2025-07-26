from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)
class MySchemaView(SpectacularAPIView):
    ...


urlpatterns = [
    # Admin
    path("iblog-management/", admin.site.urls),
    # API
    path("api/schema/", MySchemaView.as_view(), name="schema"),
    path("api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/",
         SpectacularRedocView.as_view(url_name="schema"),
         name="redoc",
         ),
    path("api/blogs/", include("core.post.urls"), name="blogs"),
    path("api/auth/", include("core.account.urls"), name="account"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


