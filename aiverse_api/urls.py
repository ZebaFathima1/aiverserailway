"""
URL configuration for aiverse_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/events/', include('events.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/users/', include('users.admin_urls')),
    path('api/registrations/', include('events.registration_urls')),
    path('api/admin/dashboard/', include('analytics.urls')),
    path('api/analytics/', include('analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Also serve media in production (for Railway)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
