from django.db import models
from django.contrib.auth.models import User
from apps.inicio.models import TipoPago
from apps.producto.models import Producto

class Proveedor(models.Model):
    nombres = models.CharField(max_length = 150)
    apellidos = models.CharField(max_length = 150)
    nit = models.CharField(max_length = 15)
    cui = models.CharField(max_length = 15)
    telefono = models.CharField(max_length = 15)
    direccion = models.CharField(max_length = 250)
    correo = models.CharField(max_length = 250)
    empresa = models.CharField(max_length = 250)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)

class Compra(models.Model):
    subtotal = models.FloatField(default = 0)
    estado = models.BooleanField(default = False)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizcion = models.DateTimeField(auto_now = True)
    proveedor_id = models.ForeignKey(Proveedor, on_delete = models.PROTECT)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)
    tipo_pago_id = models.ForeignKey(TipoPago, on_delete = models.PROTECT)

class DetalleCompra(models.Model):
    costo = models.FloatField(default = 0)
    cantidad = models.PositiveIntegerField(default = 0)
    total = models.FloatField(default = 0)
    producto_id = models.ForeignKey(Producto, on_delete = models.PROTECT)
    compra_id = models.ForeignKey(Compra, on_delete = models.CASCADE)