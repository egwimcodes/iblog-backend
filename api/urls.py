from django.urls import path, include



urlpatterns = [
    # ACCOUNTS
    path("accounts/", include("accounts.urls")),
    path("", include("post.urls")),
]
