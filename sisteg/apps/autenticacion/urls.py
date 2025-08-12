from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_autenticacion, name='autenticacion'),
    path('iniciar/', views.iniciar, name='iniciar'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('listar-rol-usuario/', views.listar_rol_usuario, name='listar_rol_usuario'),
]  