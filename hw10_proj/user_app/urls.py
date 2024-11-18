from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views


app_name = "user_app"

urlpatterns = [
    path("signup/", views.RegisterView.as_view(), name="signup"),
    path("signin/", views.loginuser, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(template_name="user_app/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="user_app/password_reset_confirm.html",
            success_url="/login/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(template_name="user_app/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
