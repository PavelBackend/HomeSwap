from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model
from .models import Posts
from .forms import PostForm
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from .documents import *
import logging

logger = logging.getLogger(__name__)

def test_logging(request):
    logger.debug("Это тестовое сообщение уровня DEBUG")
    logger.info("Это тестовое сообщение уровня INFO")
    logger.error("Это тестовое сообщение уровня ERROR")
    return HttpResponse("Проверка логирования")

User = get_user_model()

def generate_unique_slug(post):
    original_slug = slugify(post.title)
    slug = original_slug
    queryset = Posts.objects.filter(slug__startswith=original_slug).order_by('-slug')

    if queryset.exists():
        last_slug = queryset.first().slug
        try:
            slug_num = int(last_slug.split('-')[-1])
            slug = f"{original_slug}-{slug_num + 1}"
        except (ValueError, IndexError):
            slug = f"{original_slug}-1"
    
    return slug


def post_detail(request, slug):
    post = get_object_or_404(Posts, slug=slug)
    return render(request, 'posts/post_detail.html', {'post': post})

class PostsView(View):
    def get(self, request):
        logger.info('Получение списка постов')
        posts = Posts.objects.filter(available=True)
        return render(request, 'posts/posts.html', {'posts': posts})

class PostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'posts/post_create.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            
            try:
                post.user = User.objects.get(id=request.user.id)
            except ObjectDoesNotExist:
                return render(request, 'posts/post_create.html', {
                    'form': form,
                    'error': 'Пользователь не найден.'
                })
            
            post.slug = generate_unique_slug(post)

            post.save()
            return redirect('posts:post_detail', slug=post.slug)
        else:
            return render(request, 'posts/post_create.html', {'form': form})

def search_posts(request):
    q = request.GET.get('q')
    context = {}
    if q:
        posts = PostDocument.search().query(
            "bool", 
            should=[
                {"match": {"title": q}},
                {"match": {"content": q}},
            ],
            minimum_should_match=1
        )
        context['posts'] = posts
    else:
        context['posts'] = []

    return render(request, 'posts/search_posts.html', context)
