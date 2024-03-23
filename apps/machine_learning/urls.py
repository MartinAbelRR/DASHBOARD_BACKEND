from django.urls import path
from . import views

urlpatterns = [
    path('indicadores_totales/', views.get_indicadores_totales, name='get_indicadores_totales'),
    path('sucursales_x_ventas/', views.get_sucursales_x_ventas, name='get_sucursales_x_ventas'),
    path('ventas_mensual/', views.get_ventas_mensual, name='get_ventas_mensual')
]