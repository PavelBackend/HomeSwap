from django.contrib import admin
from django.urls import path, include
from main_hms import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path("auth_test/", auth_test, name="auth_test"),
    path("", index, name='index'),
    path("about/", about, name='about'),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path('registration_success/', registration_success, name='regorauth_success'),
    path("login/", LoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("posts/", include("posts.urls", namespace="posts")),
    path('chat/', include('chat.urls', namespace="chat")),
    path('api/', include('api.urls', namespace="api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
