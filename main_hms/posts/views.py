from django.http import HttpResponse
from django.shortcuts import render

def post_detail(request, slug):
    return HttpResponse('post_detail')
