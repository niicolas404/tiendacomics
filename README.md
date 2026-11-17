# Tienda de cómics

## Ejecutar el proyecto en otro computador

El proyecto incluye `catalogo/fixtures/datos_iniciales.json` con los datos
exportados de editoriales, cómics y reservas. Las imágenes referenciadas por los
cómics están en la carpeta `media/`.

En esta instalación, el entorno virtual está en `D:\TIENDA-DJANGO\.venv`,
fuera de la carpeta del repositorio. Desde `D:\TIENDA-DJANGO`, créalo solo si
aún no existe, actívalo y luego entra al repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
cd .\tiendacomics
python -m pip install -r requeriments.txt
```

Si ya estás en la carpeta del repositorio, omite `cd .\tiendacomics`. Si el
entorno virtual ya existe, omite `python -m venv .venv` y actívalo desde su
carpeta contenedora. En otros computadores, ajusta las rutas según dónde clones
el proyecto y dónde crees el entorno.

Inicia MySQL y crea una base de datos vacía llamada `tiendacomics`, como indica
la configuración de `tiendacomics/settings.py`. No es necesario iniciar Apache:
Django sirve el sitio durante el desarrollo.

Luego, todavía desde la carpeta raíz del repositorio, restaura el esquema y los
datos iniciales:

```powershell
python manage.py migrate
python manage.py loaddata datos_iniciales
python manage.py runserver
```

Carga el fixture una vez en una base de datos vacía para restaurar el conjunto
inicial. Si MySQL usa otro usuario, contraseña, host o puerto, actualiza primero
la configuración en `tiendacomics/settings.py`.

## Actualizar el fixture

Si agregas, modificas o eliminas datos desde el sitio o el panel de
administración y quieres distribuir esos cambios, vuelve a exportar el fixture
y guarda el archivo actualizado en Git:

```text
python manage.py dumpdata catalogo --indent 2 --output catalogo/fixtures/datos_iniciales.json
```