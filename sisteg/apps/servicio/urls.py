from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_servicio, name='servicio'),
    path('venta/', views.vista_venta, name='venta'),
    path('cliente/', views.vista_cliente, name='cliente'),
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('listar-cliente/', views.listar_cliente, name='listar_cliente'),
    path('agregar-servicio/', views.agregar_servicio, name='agregar_servicio'),
    path('listar-carrito/', views.listar_carrito, name='listar_carrito'),
    path('confirmar-servicio/', views.confirmar_servicio, name='confirmar_servicio'),
    path('eliminar-servicio/', views.eliminar_servicio, name='eliminar_servicio'),
    path('listar-servicios/', views.listar_servicios, name='listar_servicios'),
]