from django.urls import path
from . import views

app_name='chat'

urlpatterns = [
    path('<str:room_name>/', views.ChatView.as_view(), name='chat_room'),
]
