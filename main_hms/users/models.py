from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class User(AbstractUser):
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.username)
            queryset = User.objects.filter(slug__startswith=original_slug).count()
            if queryset:
                self.slug = f"{original_slug}-{queryset + 1}"
            else:
                self.slug = original_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.username})
