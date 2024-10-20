from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.views import View
from main_hms.settings import env
from .tasks import send_test_email
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

def get_user_slug(request):
    profile_url = reverse('users:user_detail', kwargs={'slug': request.user.slug})
    return JsonResponse({'slug': request.user.slug, 'profile_url': profile_url})


class UserDetail(View):
    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        form = UserForm(instance=user)
        context = {'slug': slug, 'user': user, 'form': form}
        return render(request, 'users/user_detail.html', context)

    def post(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        if request.user != user:
            return HttpResponseForbidden("У вас нет прав для редактирования этого профиля.")
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('users:user_detail', slug=user.slug)
        else:
            context = {'slug': slug, 'user': user, 'form': form}
            return render(request, 'users/user_detail.html', context)
        

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
