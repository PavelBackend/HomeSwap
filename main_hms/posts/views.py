from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import get_user_model
from posts.utils import generate_chat_hash
from .models import Posts
from .forms import PostForm
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from .documents import *
import logging


logger = logging.getLogger(__name__)

User = get_user_model()


def generate_unique_slug(post):
    logger.info("Генерация уникального slug поста")
    original_slug = slugify(post.title)
    slug = original_slug
    queryset = Posts.objects.filter(slug__startswith=original_slug).order_by("-slug")

    if queryset.exists():
        last_slug = queryset.first().slug
        try:
            slug_num = int(last_slug.split("-")[-1])
            slug = f"{original_slug}-{slug_num + 1}"
        except (ValueError, IndexError):
            slug = f"{original_slug}-1"

    return slug


class PostDetail(View):
    def get(self, request, slug):
        logger.info("Получение поста")
        post = get_object_or_404(Posts, slug=slug)

        author_slug = post.user.slug
        viewer_slug = request.user.slug
        chat_hash = generate_chat_hash(slug, author_slug, viewer_slug)

        context = {"post": post, "chat_hash": chat_hash}
        return render(request, "posts/post_detail.html", context)


class PostsView(View):
    def get(self, request):
        logger.info("Получение списка или поиск постов")
        query = request.GET.get("q", "").strip()
        context = {}

        try:
            if query:
                logger.info(f'Выполнение поиска по запросу: "{query}"')
                search = PostDocument.search().query(
                    "bool",
                    must=[
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title", "content"],
                            }
                        }
                    ],
                    filter=[{"term": {"available": True}}],
                )
                response = search.execute()
                posts = response.hits
                context["query"] = query
            else:
                logger.info("Отображение всех доступных постов")
                posts = Posts.objects.filter(available=True)
                context["query"] = ""

            context["posts"] = posts
        except Exception as e:
            logger.error(f"Ошибка при получении постов: {e}")
            context["posts"] = []
            context["error"] = "Произошла ошибка при загрузке постов."

        return render(request, "posts/posts.html", context)


class PostCreate(View):
    def get(self, request):
        logger.info("Отображение формы создания поста")
        form = PostForm()
        return render(request, "posts/post_create.html", {"form": form})

    def post(self, request):
        logger.info("Создание нового поста")
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            try:
                post.user = User.objects.get(id=request.user.id)
            except ObjectDoesNotExist:
                return render(
                    request,
                    "posts/post_create.html",
                    {"form": form, "error": "Пользователь не найден."},
                )

            post.slug = generate_unique_slug(post)

            post.save()
            return redirect("posts:post_detail", slug=post.slug)
        else:
            return render(request, "posts/post_create.html", {"form": form})


class PostUpdate(View):
    def get(self, request, slug):
        logger.info("Отображение формы редактирования поста")
        post = get_object_or_404(Posts, slug=slug)
        form = PostForm(instance=post)
        return render(request, "posts/post_update.html", {"form": form, "post": post})

    def post(self, request, slug):
        logger.info("Обновление поста")
        post = get_object_or_404(Posts, slug=slug)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail", slug=post.slug)
        else:
            return render(
                request, "posts/post_update.html", {"form": form, "post": post}
            )


class PostDelete(View):
    def post(self, request, slug):
        logger.info("Удаление поста")
        post = get_object_or_404(Posts, slug=slug)
        post.delete()
        logger.info("Удаление поста: %s", post.title)
        return redirect("posts:posts")
