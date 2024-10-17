from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Posts


def post_detail(request, slug):
    post = get_object_or_404(Posts, slug=slug)
    return render(request, 'posts/post_detail.html', {'post': post})


class PostsView(View):
    def get(self, request):
        posts = Posts.objects.filter(available=True)
        return render(request, 'posts/posts.html', {'posts': posts})
    
    # def post(self, request):
    #     posts = Posts.objects.all()
    #     return render(request, 'posts/posts.html', {'posts': posts})
