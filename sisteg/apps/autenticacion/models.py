from django.db import models

class TipoUsuario(models.Model):
    rol = models.CharField(max_length = 15)
    estado = models.BooleanField(default = True)