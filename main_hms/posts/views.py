from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import get_user_model
from .models import Posts
from .forms import PostForm
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from .models import Posts

User = get_user_model()

def post_detail(request, slug):
    post = get_object_or_404(Posts, slug=slug)
    return render(request, 'posts/post_detail.html', {'post': post})


class PostsView(View):
    def get(self, request):
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
            
            # Генерация уникального slug
            original_slug = slugify(post.title)
            queryset = Posts.objects.filter(slug__startswith=original_slug).count()
            if queryset:
                slug = f"{original_slug}-{queryset + 1}"
            else:
                slug = original_slug
            post.slug = slug

            post.save()
            return redirect('post_detail', slug=post.slug)
        else:
            return render(request, 'posts/post_create.html', {'form': form})
        