from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_compra, name='compra'),
    path('proveedor/', views.vista_proveedor, name='proveedor'),
    path('agregar-proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('listar-proveedor/', views.listar_proveedor, name='listar_proveedor'),
    path('agregar-compra/', views.agregar_compra, name='agregar_compra'),
    path('listar-carrito/', views.listar_carrito, name='listar_carrito'),
    path('eliminar-compra/', views.eliminar_compra, name='eliminar_compra'),
    path('confirmar-compra/', views.confirmar_compora, name='confirmar_compra'),
    path('listar-compras/', views.listar_compras, name='listar_compras'),
]