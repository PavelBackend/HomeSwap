from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from main_hms.settings import env
from .tasks import send_test_email
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer


def user_detail(request, slug):
    return render(request, 'users/user_detail.html', {'slug': slug})


def send_test_email_view(request):
    send_test_email.delay()
    return HttpResponse('Delaied email sent!')


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
