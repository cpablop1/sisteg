from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_autenticacion, name='autenticacion'),
    path('iniciar/', views.iniciar, name='iniciar'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('listar-roles/', views.listar_roles, name='listar_roles'),
    path('listar-usuarios-con-roles/', views.listar_usuarios_con_roles, name='listar_usuarios_con_roles'),
    path('usuario/', views.vista_usuario, name='usuario'),
    path('usuario-agregar/', views.agregar_usuario, name='usuario_agregar'),
    path('listar-usuario/', views.listar_usuario, name='listar_usuario'),
]  