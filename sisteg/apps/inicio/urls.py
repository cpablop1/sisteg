from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_inicio, name = 'inicio'),
    path('listar-tipo-pago/', views.listar_tipo_pago, name = 'listar_tipo_pago'),
    path('estadistica/', views.estadistica, name='estadistica'),
    path('reporte-completo-excel/', views.reporte_completo_excel, name='reporte_completo_excel'),
]