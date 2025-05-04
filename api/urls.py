from django.urls import path
from .views import RegsiterIBlogUserView
urlpatterns = [
    path("register/", RegsiterIBlogUserView.as_view(),name='register')
]
