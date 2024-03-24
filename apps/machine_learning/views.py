from django.conf import settings
import os
import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_indicadores_totales(request):
    path = os.path.join(settings.CSV_FILES_DIR, r'supermarket_sales_semi_clean.csv') # Para Deploy.
    data = pd.read_csv(path)

    dict_indicadores = dict(data[['Total', 'Costo de bienes vendidos', 'Ingreso bruto', 'Cantidad']].sum())

    list_dict_indicadores = [{
            'id': id,
            'title': key,
            'indicador': int(value),
            'porcentaje': 10,
            'increment': 3.8
    } for ((key, value), id) in zip(dict_indicadores.items(), range(len(dict_indicadores)))]
        
    return Response(list_dict_indicadores, status= status.HTTP_200_OK)    

@api_view(['GET'])
def get_ventas_mensual(request):
    path = os.path.join(settings.CSV_FILES_DIR, r'serie_supermarket_sales.csv') # Para Deploy.
    data = pd.read_csv(path)


    dict_ventas = dict(data[['MesEncoded', 'Cantidad']].groupby('MesEncoded').agg(['sum'])['Cantidad']['sum'])

    return Response({
    'labels': list(dict_ventas.keys()),
    'datasets': [
        {
            'label': 'Estadísticas de Cantidad Ventas Mensuales',
            'data': list(dict_ventas.values()),
            'fill': False,
            'backgroundColor': 'rgb(59 130 246)',
            'borderColor': 'rgb(59 130 246 / 0.5)', 
            'borderWidth': 6
        }
    ]
}, status= status.HTTP_200_OK)


@api_view(['GET'])
def get_sucursales_x_ventas(request):    
    path = os.path.join(settings.CSV_FILES_DIR, r'supermarket_sales_semi_clean.csv') # Para Deploy.
    data = pd.read_csv(path)
    
    df_ventas_sucursal = data[['Sucursal', 'Cantidad']].groupby('Sucursal').agg(['count', 'sum', 'mean'])
    
    sucursales = df_ventas_sucursal.index.to_list()
    ventas = list(df_ventas_sucursal['Cantidad']['sum'].values)

    return Response({
    'labels': sucursales,
    'datasets': [
        {
            'label': 'Ventas X Sucursal',
            'data': ventas,
            'backgroundColor': [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
            ],
            'borderColor': 'rgba(255, 99, 132, 0.2)',
            'borderWidth': 1     
        },
    ]}, status= status.HTTP_200_OK)