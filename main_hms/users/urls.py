from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('<slug:slug>/', views.user_detail, name='user_detail'),
]