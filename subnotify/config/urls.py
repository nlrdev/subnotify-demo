from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portal.views import (
    logout,
    login,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("", include("portal.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)