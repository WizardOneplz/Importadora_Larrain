from django.shortcuts import render
from django.db import connection

# Create your views here.

def mantenedor_productos(request):
    data = {
        'marcas':listado_marcas()
    }
    return render(request, 'mantenedor_productos.html',data)

def listado_marcas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_MARCAS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista