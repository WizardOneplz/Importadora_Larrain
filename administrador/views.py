from django.shortcuts import render
from django.db import connection
import cx_Oracle 

# Create your views here.

def mantenedor_admin(request):
    data = {
        'empleados':listar_empleados(),
        'cargos':listar_cargos(),
        'cliente':listado_clientes(),
    }
    if request.method== 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        ap_paterno = request.POST.get('ap_paterno')
        ap_materno = request.POST.get('ap_materno')
        genero = request.POST.get('genero')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        cargo = request.POST.get('cargo')
        salida = agregar_empleado(rut, nombre, ap_paterno, ap_materno, genero, telefono, email, cargo)
        if salida==1:
            data['mensaje'] = 'Empleado registrado correctamente'
        else:
            data['mensaje'] = 'No se ha podido registrar al Empleado'
    return render(request, 'agregar_empleado.html',data)

def agregar_empleado(rut,nombre,ap_paterno,ap_materno,genero,telefono,email,cargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('ADM_AGREGAR_EMPLEADO',[rut, nombre, ap_paterno, ap_materno, genero, telefono, email, cargo, salida])
    return salida.getvalue()

def listar_empleados():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("ADM_LISTAR_EMPLEADOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista
    

def listar_cargos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("ADM_LISTAR_CARGOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_clientes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur =django_cursor.connection.cursor()

    cursor.callproc("LISTAR_DATOS",[out_cur])

    lista =[]
    for fila in out_cur:
        lista.append(fila)
    return lista