from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = "user_app"

urlpatterns = [
    path("signup/", views.RegisterView.as_view(), name="signup"),
    path("signin/", views.loginuser, name="login"),
    path("logout/", views.logoutuser, name="logout"),
]
