from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from main_hms.settings import env
from .tasks import send_test_email


def user_detail(request, slug):
    return render(request, 'users/user_detail.html', {'slug': slug})


def send_test_email_view(request):
    send_test_email.delay()
    return HttpResponse('Delaied email sent!')

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
