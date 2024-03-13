from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('todolist/', include('todolist.urls', namespace='todolist')),
    path('todolist/v2/', include('todolist.v2.urls', namespace='todolist-v2')),
    path('todolist/v3/', include('todolist.v3.urls', namespace='todolist-v3')),
    path('shorturl/', include('url_shortener.urls', namespace='url_shortener')),
    path('', include('frontend.urls', namespace='frontend')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
