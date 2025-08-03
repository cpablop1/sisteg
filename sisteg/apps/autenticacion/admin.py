from django.contrib import admin
from .models import Rol, RolUsuario

class AdminRol (admin.ModelAdmin):
    list_display = ['id', 'rol', 'estado']
    readonly_fields = ['id']

admin.site.register(Rol, AdminRol)

class AdminRolUsuario (admin.ModelAdmin):
    list_display = ['id', 'obtener_usuario', 'obtener_nombre_rol']
    readonly_fields = ['id'] 

    def obtener_nombre_rol(self, obj):
        return obj.rol_id.rol  # Ajusta el campo según el nombre real en tu modelo relacionado
    obtener_nombre_rol.admin_order_field = 'rol_id'  # Permite ordenar por este campo
    obtener_nombre_rol.short_description = 'rol'  # Nombre amigable en la tabla
    
    def obtener_usuario(self, obj):
        return obj.usuario_id.username  # Ajusta el campo según el nombre real en tu modelo relacionado
    obtener_usuario.admin_order_field = 'usuario_id'  # Permite ordenar por este campo
    obtener_usuario.short_description = 'usuario'  # Nombre amigable en la tabla


admin.site.register(RolUsuario, AdminRolUsuario)