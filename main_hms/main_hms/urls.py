from django.contrib import admin
from django.urls import path, include, reverse_lazy
from main_hms import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path("auth_test/", auth_test, name="auth_test"),
    path("", index, name='home'),
    path("about/", about, name='about'),

    path('password-reset/',
        PasswordResetView.as_view(
            template_name='main_hms/password_reset_form.html',
            email_template_name='main_hms/password_reset_email.html',
            success_url=reverse_lazy('password-reset-done')),
            name='password-reset'),

    path('password-reset/done/',
        PasswordResetDoneView.as_view(
            template_name='main_hms/password_reset_done.html'),
            name='password-reset-done'),
            
    path("register/", UserRegistrationView.as_view(), name="user_registration"),

    path('password-reset/<uidb64>/<token>/', 
        CustomPasswordResetConfirmView.as_view(),
            name='password-reset-confirm'),

    path('password-reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='main_hms/password_reset_complete.html'),
            name='password-reset-complete'),

    path('registration_success/', registration_success, name='reg_success'),
    path('authorization_success/', auth_success, name='auth_success'),
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
