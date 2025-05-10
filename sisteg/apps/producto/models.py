from django.db import models
from django.contrib.auth.models import User

class Marca(models.Model):
    descripcion = models.CharField(max_length = 100)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)

class Categoria(models.Model):
    descripcion = models.CharField(max_length = 100)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)

class Producto(models.Model):
    descripcion = models.CharField(max_length = 250)
    detalle = models.TextField()
    costo = models.FloatField(default = 0)
    precio = models.FloatField(default = 0)
    stock = models.PositiveIntegerField(default = 0)
    img1 = models.ImageField(upload_to = 'producto', blank = True, null = True) 
    img2 = models.ImageField(upload_to = 'producto', blank = True, null = True)
    estado = models.BooleanField(default = True)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    marca_id = models.ForeignKey(Marca, on_delete = models.PROTECT)
    categoria_id = models.ForeignKey(Categoria, on_delete = models.PROTECT)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)