from django.db import models
from django.contrib.auth.models import User

class TipoPago(models.Model):
    descripcion = models.CharField(max_length = 100)
    fecha_ingreso = models.DateTimeField(auto_now_add = True)
    fecha_actualizacion = models.DateTimeField(auto_now = True)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)