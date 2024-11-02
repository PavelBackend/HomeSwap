from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.views import View
from main_hms.settings import env
from posts.models import Posts
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


def get_user_slug(request):
    logger.info('Получение slug пользователя')
    profile_url = reverse('users:user_detail', kwargs={'slug': request.user.slug})
    return JsonResponse({'slug': request.user.slug, 'profile_url': profile_url})


class UserDetail(LoginRequiredMixin, View):
    def get(self, request, slug):
        logger.info('Получение страницы пользователя')
        user = get_object_or_404(User, slug=slug)
        if request.user != user:
            return render(request, 'main_hms/access_denied.html')
        form = UserForm(instance=user)
        user_posts = Posts.objects.filter(user=user)
        context = {'slug': slug, 'user': user, 'form': form, 'user_posts': user_posts}
        return render(request, 'users/user_detail.html', context)

    def post(self, request, slug):
        logger.info('Обновление профиля пользователя')
        user = get_object_or_404(User, slug=slug)

        if request.user != user:
            return render(request, 'main_hms/access_denied.html')
        
        form = UserForm(request.POST, request.FILES,instance=user)
        
        if form.is_valid():
            logger.info('Успешное обновление профиля пользователя')
            form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('users:user_detail', slug=user.slug)
        else:
            logger.info('Неудачное обновление профиля пользователя')
            user_posts = Posts.objects.filter(user=user)
            context = {'slug': slug, 'user': user, 'form': form, 'user_posts': user_posts}
            return render(request, 'users/user_detail.html', context)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        logger.info('Регистрация пользователя')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
