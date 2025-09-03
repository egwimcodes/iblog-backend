from django.urls import path
from core.account.views import AuthView, UserAccountManagementView


urlpatterns = [
    # Update Update
    path('register/', AuthView.as_view({'post': 'register'}), name='register'),
    path('login/', AuthView.as_view({'post': 'login'}), name='login'),
    path('google_login/',
         AuthView.as_view({'post': 'google_login'}), name='google_login'),
    path('password_reset/',
         AuthView.as_view({'post': 'password_reset'}), name='password_reset'),
    path('password_reset_done/',
         AuthView.as_view({'post': 'password_reset_done'}), name='password_reset_done'),

    path("me/", UserAccountManagementView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update'
    }), name="me"),
    path('me/logout/', AuthView.as_view({'post': 'logout'}), name='logout'),
]
