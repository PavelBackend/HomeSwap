from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Функция для генерации уникального slug
def generate_unique_slug(post):
    # Преобразуем заголовок поста в slug
    original_slug = slugify(post.title)
    slug = original_slug
    queryset = Posts.objects.filter(slug__startswith=original_slug).order_by('-slug')

    # Если уже существуют посты с похожим slug, добавляем числовой суффикс
    if queryset.exists():
        last_slug = queryset.first().slug
        try:
            # Извлекаем последний суффикс из найденного slug
            slug_num = int(last_slug.split('-')[-1])
            slug = f"{original_slug}-{slug_num + 1}"
        except (ValueError, IndexError):
            # Если нет числового суффикса, просто добавляем "-1"
            slug = f"{original_slug}-1"
    
    return slug


class Posts(models.Model):
    title = models.CharField("Title" ,max_length=100, null=False, blank=False)
    slug = models.SlugField("Slug", max_length=100, blank=True, unique=True)
    image_url = models.TextField("Image URL", null=True, blank=True)
    content = models.TextField("Content", max_length=1500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField("Available", default=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class PostsManager(models.Manager):

    def get_queryset(self): 
        return super(PostsManager, self).get_queryset().select_related('user').filter(available=True)
    

class PostsProxy(Posts):

    objects = PostsManager()

    class Meta:
        proxy = True
