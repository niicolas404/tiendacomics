import uuid
from django.core.validators import MinValueValidator
from django.db import models
from .validators import validar_rut

# Create your models here.
class Editorial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=200, blank=True)

    
    def __str__(self):
        return self.nombre

class Comic(models.Model):
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    fecha_publicacion = models.DateField()
    portada = models.ImageField(upload_to='portadas/')
    precio = models.PositiveIntegerField()
    tomo = models.PositiveIntegerField()
    material = models.BooleanField(default=False, verbose_name="¿Es tapa dura?")
    stock = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True, verbose_name="¿Disponible en el catálogo público?")

    def __str__(self):
        return self.titulo

    def precio_chileno(self):
        return f"${self.precio:,}".replace(",", ".")

class Reserva(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=50)
    correo_cliente = models.EmailField(max_length=50)
    rut_cliente = models.CharField(max_length=12, validators=[validar_rut])
    cantidad_ejemplares = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


    def __str__(self):
        return f"Reserva de {self.nombre_cliente} ({self.rut_cliente}) para {self.comic.titulo}"