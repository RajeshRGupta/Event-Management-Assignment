from django.urls import path
from .views import LoginView, ProfileView, RegisterView
from rest_framework_simplejwt.views import  TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("profile/", ProfileView.as_view()),
]
