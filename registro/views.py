from django.shortcuts import render
from django.db import connection
from core.models import Cliente, CuentaCliente, Rol
import getpass
import cx_Oracle
# Create your views here.

def registro(request):
    data = {
        'CIUDAD':listar_ciudad()  
    }
    if request.method== 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        ap_paterno = request.POST.get('ap_paterno')
        ap_materno = request.POST.get('ap_materno')
        genero = request.POST.get('genero')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('Direccion')
        ciudad = request.POST.get('ciudad')
        clave= request.POST.get('clave')
        salida = agregar_cliente(rut, nombre, ap_paterno, ap_materno, genero, telefono, email, direccion, clave, ciudad)
        if salida==1:
            data['mensaje'] = 'Cliente Registrado Correctamente'
        else:
            data['mensaje'] = 'No se ha podido registrar al Cliente'
    return render(request, 'registro.html' , data)

def agregar_cliente(rut,nombre,ap_paterno,ap_materno,genero,telefono,email,direccion,clave,ciudad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('AGREGAR_CLIENTE',[rut, nombre, ap_paterno, ap_materno, genero, telefono, email, direccion, clave, ciudad, salida])
    return salida.getvalue()

def listar_ciudad():
     
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_CIUDAD", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila) 
    return lista