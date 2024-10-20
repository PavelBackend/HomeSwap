from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('get-user-slug/', views.get_user_slug, name='get_user_slug'),
    # path('send_test_email_view', views.send_test_email_view, name='send_test_email_view'),
    path('profile/<slug:slug>/', views.UserDetail.as_view(), name='user_detail'),
]