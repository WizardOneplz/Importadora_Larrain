from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.

def mantenedor_productos(request):
    data = {
        'marcas':listado_marcas()
    }

    #agregar_marca(4,'Genius')

    if request.method== 'POST':
        id = request.POST.get('id')
        nombre_marca = request.POST.get('nombre_marca')
        salida = agregar_marca(id, nombre_marca)
        if salida==1:
            data['mensaje'] = 'Marca registrada correctamente'
            data['marcas'] = listado_marcas()
        else:
            data['mensaje'] = 'No se ha podido registrar la Marca'

    if request.method== 'POST':
        id_categoria = request.POST.get('id_categoria')
        nombre_categoria = request.POST.get('nombre_categoria')
        salida = agregar_categoria(id_categoria, nombre_categoria)
        if salida==1:
            data['mensaje'] = 'Categoria registrada correctamente'
        else:
            data['mensaje'] = 'No se ha podido registrar la Categoria'  

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

def agregar_marca(id, nombre_marca):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_MARCA',[id, nombre_marca, salida])
    return salida.getvalue()

def agregar_categoria(id_categoria, nombre_categoria):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CATEGORIA',[id_categoria, nombre_categoria, salida])
    return salida.getvalue()