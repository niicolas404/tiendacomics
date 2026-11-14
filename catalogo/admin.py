from django.contrib import admin
from catalogo.models import Comic, Editorial, Reserva


class ComicAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha_publicacion', 'precio_chileno', 'tomo', 'material', 'stock', 'editorial', 'disponible_texto']
    list_filter = ['titulo', 'editorial', 'material']
    search_fields = ['titulo', 'autor', 'editorial__nombre']

    @admin.display(description="Disponibilidad")
    def disponible_texto(self, obj):
        return "Sí" if obj.disponible else "No"


class EditorialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    list_filter = ['nombre']
    search_fields = ['nombre']

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'comic', 'nombre_cliente', 'rut_cliente', 'cantidad_ejemplares', 'fecha_reserva']
    list_filter = ['nombre_cliente', 'rut_cliente', 'comic']
    search_fields = ['nombre_cliente', 'rut_cliente']

admin.site.register(Comic, ComicAdmin)
admin.site.register(Editorial, EditorialAdmin)
admin.site.register(Reserva, ReservaAdmin)
