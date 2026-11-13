from django.contrib import admin
from catalogo.models import Comic, Editorial


class ComicAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha_publicacion', 'precio_chileno', 'tomo', 'material', 'stock', 'editorial']
    list_filter = ['titulo', 'editorial', 'material']
    search_fields = ['titulo', 'autor', 'editorial__nombre']


class EditorialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    list_filter = ['nombre']
    search_fields = ['nombre']

admin.site.register(Comic, ComicAdmin)
admin.site.register(Editorial, EditorialAdmin)
