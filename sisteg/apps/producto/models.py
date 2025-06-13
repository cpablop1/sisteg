from django.db import models
from django.contrib.auth.models import User

import os

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
    img1 = models.ImageField(upload_to = 'producto', blank = True) 
    img2 = models.ImageField(upload_to = 'producto', blank = True)
    estado = models.BooleanField(default = True)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    marca_id = models.ForeignKey(Marca, on_delete = models.PROTECT)
    categoria_id = models.ForeignKey(Categoria, on_delete = models.PROTECT)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)

    def save(self, *args, **kwargs):
        # Verificar si el objeto ya existe en la base de datos
        if self.pk:
            try:
                old_img_1 = Producto.objects.get(pk=self.pk).img1
                old_img_2 = Producto.objects.get(pk=self.pk).img2
                # Comparar si la imagen ha cambiado
                if old_img_1 and old_img_1 != self.img1:
                    if os.path.isfile(old_img_1.path):
                        os.remove(old_img_1.path)  # Elimina la imagen anterior
                
                if old_img_2 and old_img_2 != self.img2:
                    if os.path.isfile(old_img_2.path):
                        os.remove(old_img_2.path)  # Elimina la imagen anterior
                        
            except Producto.DoesNotExist:
                pass  # El objeto es nuevo, no hay imagen anterior

        super().save(*args, **kwargs)  # Guarda el objeto normalmente