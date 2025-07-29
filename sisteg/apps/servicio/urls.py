from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_servicio, name='servicio'),
    path('venta/', views.vista_venta, name='venta'),
    path('cliente/', views.vista_cliente, name='cliente'),
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('listar-cliente/', views.listar_cliente, name='listar_cliente'),
]