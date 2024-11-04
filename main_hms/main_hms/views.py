from django.shortcuts import render
from django.contrib.auth import get_user_model
import logging
from django.contrib.auth.views import PasswordResetConfirmView


User = get_user_model()

logger = logging.getLogger(__name__)


def index(request):
    logger.info("Главная страница")
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    context = {"user": user, "title": "Main page"}
    return render(request, "main_hms/index.html", context)


def about(request):
    logger.info("О нас")
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    context = {"user": user, "title": "How it works"}
    return render(request, "main_hms/about.html", context)
