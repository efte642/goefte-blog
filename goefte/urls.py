from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # Include URLs from your app (core_app)
    path("", include(("core_app.urls", "core_app"), namespace="core_app")),

    # CKEditor file upload URL
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
