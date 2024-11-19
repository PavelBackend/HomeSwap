import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from main_hms import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("reg_auth.urls", namespace="reg_auth")),
    path("users/", include("users.urls", namespace="users")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("chat/", include("chat.urls", namespace="chat")),
    path("payment/", include("payment.urls", namespace="payment")),
    # path("api/", include("api.urls", namespace="api")),
    path("", index, name="home"),
    path("about/", about, name="about"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
