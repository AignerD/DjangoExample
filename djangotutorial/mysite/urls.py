from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, save_audio

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("save_audio/", save_audio, name="save_audio"),  # New API endpoint
]

# ✅ Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
