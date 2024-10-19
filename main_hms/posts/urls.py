from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('create/', views.PostCreate.as_view() , name='create_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]