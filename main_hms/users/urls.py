from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('send_test_email_view', views.send_test_email_view, name='send_test_email_view'),
    path('<slug:slug>/', views.user_detail, name='user_detail'),
]