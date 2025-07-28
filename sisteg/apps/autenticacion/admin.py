from django.contrib import admin
from .models import Rol, RolUsuario

class AdminRol (admin.ModelAdmin):
    list_display = ['id', 'rol', 'estado']
    readonly_fields = ['id']

admin.site.register(Rol, AdminRol)

class AdminRolUsuario (admin.ModelAdmin):
    list_display = ['id', 'obtener_nombre_rol']
    readonly_fields = ['id']

    def obtener_nombre_rol(self, obj):
        print('\n----------------------------------')
        print(obj)
        print('----------------------------------\n')
        return obj.rol_id.rol  # Ajusta el campo según el nombre real en tu modelo relacionado
    obtener_nombre_rol.admin_order_field = 'rol_id'  # Permite ordenar por este campo
    obtener_nombre_rol.short_description = 'rol'  # Nombre amigable en la tabla


admin.site.register(RolUsuario, AdminRolUsuario)