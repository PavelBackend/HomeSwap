from django.shortcuts import render


def index(request):
    return render (request, 'main_hms/index.html', {'title': 'Main page'})


def about(request):
    return render (request, 'main_hms/about.html', {'title': 'How it works'})
