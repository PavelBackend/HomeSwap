from django.db import models
from django.urls import reverse


class Posts(models.Model):
    title = models.CharField("Title" ,max_length=100, null=False, blank=False)
    slug = models.SlugField("Slug", max_length=100, null=False, blank=False, unique=True)
    image_url = models.TextField("Image URL", null=True, blank=True)
    content = models.TextField("Content", max_length=1500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField("Available", default=True)

    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='posts')

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
