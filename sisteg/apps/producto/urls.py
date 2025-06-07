from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_producto, name='producto'),
    path('categoria/', views.vista_categoria, name='categoria'),
    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('listar-categoria/', views.listar_categoria, name='listar_categoria'),
    path('marca/', views.vista_marca, name='marca'),
    path('agregar-marca/', views.agregar_marca, name='agregar_marca'),
    path('listar-marca/', views.listar_marca, name='listar_marca'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('listar-producto/', views.listar_producto, name='listar_producto'),
]