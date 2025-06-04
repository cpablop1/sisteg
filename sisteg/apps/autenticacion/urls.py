from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_autenticacion, name='autenticacion'),
    path('iniciar/', views.iniciar, name='iniciar'),
    path('cerrar/', views.cerrar, name='cerrar'),
]  