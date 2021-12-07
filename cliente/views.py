from django.shortcuts import render
from django.db import connection
import cx_Oracle
# Create your views here.

def modificar_datos(request):
    return render(request, 'modificar_datos.html')

def listar_datos(request):
    data = {
        'CLIENTE':listado_clientes()
    }
    return render(request, 'listar_datos.html',data)

def listado_clientes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur =django_cursor.connection.cursor()

    cursor.callproc("LISTAR_DATOS",[out_cur])

    lista =[]
    for fila in out_cur:
        lista.append(fila)
    return lista

def listar_ciudad():
     
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_CIUDAD", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila) 
    return lista
