from django.http import HttpResponse
from django.shortcuts import render

def post_detail(request, slug):
    return render(request, 'posts/post_detail.html', {'slug': slug})
