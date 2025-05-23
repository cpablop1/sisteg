from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_producto, name='producto'),
    path('categoria/', views.vista_categoria, name='categoria'),
    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('listar-categoria/', views.listar_categoria, name='listar_categoria'),
]  