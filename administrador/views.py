from django.shortcuts import render, redirect
from django.db import connection
from core.models import Empleado,CuentaEmpleado, Rol
import cx_Oracle 

# Create your views here.

#EMPLEADOS
def mantenedor_admin(request):
    data = {
        'cargos':listar_cargos(),
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
        'productos':listar_productos(),
        'cliente':listado_clientes(),
        'empleados':listado_empleados(),
        'listar_empleados':Empleado.objects.all(),
        'bodega':listado_bodega(),
        'pasillo':listado_pasillo(),
        'estanteria':listado_estanteria()
    }
 
#AGREGAR EMPLEADO
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
            data['empleados'] = listado_empleados()
        else:
            data['mensaje'] = 'No se ha podido registrar al Empleado'

#AGREGAR BODEGA
    if request.method== 'POST':
        cant_pasillos = request.POST.get('cant_pasillos')
        direccion = request.POST.get('direccion')

        salida = agregar_bodega(cant_pasillos,direccion)
        if salida==1:
            data['mensaje'] = 'Bodega registrada correctamente'
            data['bodega'] = listado_bodega()
        else:
            data['mensaje'] = 'No se ha podido registrar la bodega'

#AGREGAR PASILLO
    if request.method== 'POST':
        cant_estanterias = request.POST.get('cant_estanterias')
        id_bodega = request.POST.get('id_bodega')

        salida = agregar_pasillo(cant_estanterias,id_bodega)
        if salida==1:
            data['mensaje'] = 'Pasillo registrado correctamente'
            data['pasillo'] = listado_pasillo()
        else:
            data['mensaje'] = 'No se ha podido registrar el pasillo'

#AGREGAR ESTANTERIA

    return render(request, 'agregar_empleado.html',data)


#METODOS

#EMPLEADO
def agregar_empleado(rut,nombre,ap_paterno,ap_materno,genero,telefono,email,cargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('ADM_AGREGAR_EMPLEADO',[rut, nombre, ap_paterno, ap_materno, genero, telefono, email, cargo, salida])
    return salida.getvalue()

def listado_empleados():
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

def eliminar_empleado(request, rut):
    cuentaempleado = CuentaEmpleado.objects.get(empleado_rut=rut)
    cuentaempleado.delete()
    empleado = Empleado.objects.get(rut=rut)
    empleado.delete()

    return redirect('/agregar_empleado')

def modificar_empleado(request, rut):
    data = {
        'empleados':Empleado.objects.get(rut=rut),
        'cargos':listar_cargos()
    }
    
    return render(request, "modificar_empleado.html",data)

def editar_empleado(request):
    
    rut = request.POST.get('rut')
    id = request.POST.get('id')
    nombre = request.POST.get('nombre')
    ap_paterno = request.POST.get('ap_paterno')
    ap_materno = request.POST.get('ap_materno')
    genero = request.POST.get('genero')
    telefono = request.POST.get('telefono')
    email = request.POST.get('email')
    cargo = request.POST.get('cargo')
      
    empleado = Empleado.objects.get(rut=rut)
    empleado.rut = rut
    empleado.id = id 
    empleado.nombre = nombre
    empleado.apellido_paterno = ap_paterno
    empleado.apellido_materno = ap_materno
    empleado.genero = genero
    empleado.telefono = telefono
    empleado.email = email
    empleado.cargo = cargo
    empleado.save()

    return redirect('/agregar_empleado')
#CLIENTE

def listado_clientes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_DATOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

#PRODUCTOS

def listar_productos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listar_marcas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_MARCAS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listar_categorias():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_CATEGORIAS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

#BODEGA

def agregar_bodega(cant_pasillos,direccion):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('ADM_AGREGAR_BODEGA',[cant_pasillos, direccion, salida])
    return salida.getvalue()

def listado_bodega():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_BODEGA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def eliminar_empleado(request, rut):
    cuentaempleado = CuentaEmpleado.objects.get(empleado_rut=rut)
    cuentaempleado.delete()
    empleado = Empleado.objects.get(rut=rut)
    empleado.delete()

    return redirect('/agregar_empleado')

#PASILLO

def agregar_pasillo(cant_estanterias,id_bodega):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('ADM_AGREGAR_PASILLO',[cant_estanterias,id_bodega, salida])
    return salida.getvalue()

def listado_pasillo():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_PASILLO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

#ESTANTERIA

def listado_estanteria():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_ESTANTERIA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista