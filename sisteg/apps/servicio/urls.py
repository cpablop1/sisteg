from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_servicio, name='servicio'),
    path('cliente/', views.vista_cliente, name='cliente'),
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),
]