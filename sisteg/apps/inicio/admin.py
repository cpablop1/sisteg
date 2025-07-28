from django.contrib import admin
from .models import TipoPago

class AdminTipoPago (admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'fecha_ingreso', 'fecha_actualizacion', 'usuario_id']
    list_display = ['id', 'descripcion', 'fecha_ingreso', 'fecha_actualizacion', 'usuario_id']
    readonly_fields = ['id']

admin.site.register(TipoPago, AdminTipoPago)