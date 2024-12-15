from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.views import View
from .serializers import RegistrationSerializer
import logging
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import SetPasswordForm


User = get_user_model()

logger = logging.getLogger(__name__)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "reg_auth/password_reset_confirm.html"
    success_url = reverse_lazy("reg_auth:password-reset-complete")
    form_class = SetPasswordForm


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def get(self, request, *args, **kwargs):
        logger.info("Пользователь зашел на страницу регистрации")
        return render(request, "reg_auth/register.html", {"title": "Регистрация"})

    def post(self, request, *args, **kwargs):
        logger.info("Пользователь отправил данные на регистрацию")
        logger.info("Полученные данные: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info("Валидация прошла успешно")
            user = serializer.save()
            logger.info(
                "Пользователь успешно сохранён: %s", user
            )
            return redirect("reg_auth:reg_success")
        else:
            logger.warning("Ошибки валидации: %s", serializer.errors)
            return render(request, "reg_auth/register.html", {"errors": serializer.errors})


def registration_success(request):
    logger.info("Пользователь прошел регистрацию")
    return render(
        request, "reg_auth/success_reg.html", {"title": "Регистрация прошла успешно"}
    )


class LoginView(View):
    def get(self, request):
        logger.info("Пользователь зашел на страницу входа")
        return render(request, "reg_auth/login.html")

    def post(self, request):
        logger.info("Пользователь отправил данные на вход")
        email = request.POST.get("email")
        password = request.POST.get("password")

        logger.info("Попытка входа с email: %s", email)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            logger.info("Пользователь вошел: %s", user.email)
            return redirect("reg_auth:auth_success")
        else:
            logger.warning("Неверные учетные данные для email: %s", email)
            error = "Неправильный email или пароль."
            return render(request, "reg_auth/login.html", {"error": error})


def auth_success(request):
    logger.info("Пользователь прошел вход")
    return render(
        request, "reg_auth/success_auth.html", {"title": "Авторизация прошла успешно"}
    )


def access_denied(request):
    logger.info("Пользователь не авторизован")
    return render(request, "main_hms/access_denied.html")


class UserLogoutView(View):
    def get(self, request):
        logger.info("Пользователь вышел из аккаунта")
        logout(request)
        return redirect("home")
