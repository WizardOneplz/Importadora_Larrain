from django.shortcuts import render
from django.db import connection

# Create your views here.

def agregar_empleado(request):
    data = {
        'empleados':listar_empleados()
    }
    return render(request, 'agregar_empleado.html',data)

def listar_empleados():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("ADM_LISTAR_EMPLEADOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista