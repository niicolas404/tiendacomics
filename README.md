# Tienda de cómics

## Restaurar los datos iniciales

El proyecto incluye `catalogo/fixtures/datos_iniciales.json` con los datos
exportados de editoriales, cómics y reservas. Las imágenes referenciadas por los
cómics están en la carpeta `media/`.

En un computador nuevo:

1. Instala las dependencias con `pip install -r requeriments.txt`.
2. Configura y crea la base de datos MySQL indicada en
   `tiendacomics/settings.py`.
3. Ejecuta las migraciones y carga el fixture:

   ```text
   python manage.py migrate
   python manage.py loaddata datos_iniciales
   ```

4. Inicia el sitio con `python manage.py runserver`.

Carga el fixture en una base de datos vacía para restaurar el conjunto inicial.

## Actualizar el fixture

Si agregas, modificas o eliminas datos desde el sitio o el panel de
administración y quieres distribuir esos cambios, vuelve a exportar el fixture
y guarda el archivo actualizado en Git:

```text
python manage.py dumpdata catalogo --indent 2 --output catalogo/fixtures/datos_iniciales.json
```
