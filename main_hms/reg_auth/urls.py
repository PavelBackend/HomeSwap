from django.urls import path, reverse_lazy
from .views import (
    UserRegistrationView,
    registration_success,
    auth_success,
    CustomPasswordResetConfirmView,
    LoginView,
    UserLogoutView,
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

app_name = "reg_auth"

urlpatterns = [
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="reg_auth/password_reset_form.html",
            email_template_name="reg_auth/password_reset_email.html",
            success_url=reverse_lazy("reg_auth:password-reset-done"),
        ),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="reg_auth/password_reset_done.html"
        ),
        name="password-reset-done",
    ),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path(
        "password-reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="reg_auth/password_reset_complete.html"
        ),
        name="password-reset-complete",
    ),
    path("registration_success/", registration_success, name="reg_success"),
    path("authorization_success/", auth_success, name="auth_success"),
    path("login/", LoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
]