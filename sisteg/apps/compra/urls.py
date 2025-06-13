from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_compra, name='compra'),
    path('proveedor/', views.vista_proveedor, name='proveedor'),
]