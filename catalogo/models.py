from django.db import models

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
    

    def __str__(self):
        return self.titulo

    def precio_chileno(self):
        return f"${self.precio:,}".replace(",", ".")