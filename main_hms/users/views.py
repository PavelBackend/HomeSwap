from django.shortcuts import render
from django.http import HttpResponse


def user_detail(request, slug):
    return HttpResponse('user_detail')
