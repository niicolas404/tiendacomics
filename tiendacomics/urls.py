
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from catalogo import views
from tiendacomics import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, name='catalogo_inicio'),
    path('reservar/<int:comic_id>', views.reservar),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
