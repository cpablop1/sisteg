from django.db import models
from django.contrib.auth.models import User
from apps.inicio.models import TipoPago
from apps.producto.models import Producto

class Cliente(models.Model):
    nombres = models.CharField(max_length = 150)
    apellidos = models.CharField(max_length = 150)
    nit = models.CharField(max_length = 15)
    cui = models.CharField(max_length = 15)
    telefono = models.CharField(max_length = 15)
    direccion = models.CharField(max_length = 250)
    correo = models.CharField(max_length = 250)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)

class TipoServicio(models.Model):
    descripcion = models.CharField(max_length = 250)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)

class Servicio(models.Model):
    subtotal = models.FloatField(default = 0)
    costo_servicio = models.FloatField(default = 0)
    observacion = models.TextField()
    estado = models.BooleanField(default = 0)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    factura_emitida = models.BooleanField(default = False)
    tipo_servicio_id = models.ForeignKey(TipoServicio, on_delete = models.PROTECT)
    cliente_id = models.ForeignKey(Cliente, on_delete = models.PROTECT)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)
    tipo_pago_id = models.ForeignKey(TipoPago, on_delete = models.PROTECT)

class DetalleServicio(models.Model):
    precio = models.FloatField(default = 0)
    costo = models.FloatField(default = 0)
    cantidad = models.PositiveIntegerField(default = 0)
    total = models.FloatField(default = 0)
    ganancia = models.FloatField(default = 0)
    producto_id = models.ForeignKey(Producto, on_delete = models.PROTECT)
    servicio_id = models.ForeignKey(Servicio, on_delete = models.CASCADE)

class ServicioUsuario(models.Model):
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)
    servicio_id = models.ForeignKey(Servicio, on_delete = models.PROTECT)

class Garantia(models.Model):
    subtotal = models.FloatField(default = 0)
    observacion = models.TextField()
    nota = models.TextField()
    perdida = models.BooleanField(default = False)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    servicio_id = models.ForeignKey(Servicio, on_delete = models.PROTECT)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)

class DetalleGarantia(models.Model):
    precio = models.FloatField(default = 0)
    costo = models.FloatField(default = 0)
    cantidad = models.PositiveIntegerField(default = 0)
    total = models.FloatField(default = 0)
    producto_id = models.ForeignKey(Producto, on_delete = models.PROTECT)
    garantia_id = models.ForeignKey(Garantia, on_delete = models.CASCADE)

class Factura(models.Model):
    subtotal = models.FloatField(default = 0)
    descripcion = models.TextField()
    no_autorizacion = models.CharField(max_length = 60)
    bien_servicio = models.CharField(
        max_length = 1,
        choices = [
            ('B', 'Bien'),
            ('S', 'Servicio'),
        ],
        default = 'S'
    )
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    servicio_id = models.ForeignKey(Servicio, on_delete = models.PROTECT)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)