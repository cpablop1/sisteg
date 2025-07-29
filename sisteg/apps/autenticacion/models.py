from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    rol = models.CharField(max_length = 15)
    estado = models.BooleanField(default = True)

    def __str__(self):
        return self.rol

class RolUsuario(models.Model):
    rol_id = models.ForeignKey(Rol, on_delete = models.PROTECT)
    usuario_id = models.ForeignKey(User, on_delete = models.PROTECT)