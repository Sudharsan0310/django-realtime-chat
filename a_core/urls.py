from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from a_home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('a_rtchat.urls')),
    path('profile/', include('a_users.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)