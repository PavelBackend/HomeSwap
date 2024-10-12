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