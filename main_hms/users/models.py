from django.db import models
from django.urls import reverse


class Users(models.Model):
    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=50, blank=False, null=False, unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.username})
    