from django.contrib import admin
from catalogo.models import Comic, Editorial, Reserva


class ComicAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha_publicacion', 'precio_chileno', 'tomo', 'material', 'stock', 'editorial', 'disponible']
    list_filter = ['titulo', 'editorial', 'material', 'disponible']
    search_fields = ['titulo', 'autor', 'editorial__nombre']

class EditorialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    list_filter = ['nombre']
    search_fields = ['nombre']

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'comic', 'nombre_cliente', 'rut_cliente', 'correo_cliente', 'cantidad_ejemplares', 'fecha_reserva']
    list_filter = ['nombre_cliente', 'rut_cliente', 'comic']
    search_fields = ['nombre_cliente', 'rut_cliente']

admin.site.register(Comic, ComicAdmin)
admin.site.register(Editorial, EditorialAdmin)
admin.site.register(Reserva, ReservaAdmin)
