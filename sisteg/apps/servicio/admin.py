from django.contrib import admin
from .models import TipoServicio


class AdminTipoServicio (admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'fecha_ingreso', 'fecha_actualizacion']
    list_display = ['id', 'descripcion', 'fecha_ingreso', 'fecha_actualizacion']
    readonly_fields = ['id']

admin.site.register(TipoServicio, AdminTipoServicio)