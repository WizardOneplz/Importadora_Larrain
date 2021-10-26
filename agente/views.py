from django.shortcuts import render
from django.db import connection
import cx_Oracle

# Create your views here.

def subir_oferta(request):
    data = {
        'ofertas':listado_ofertas()
    }

    if request.method == 'POST':
        ID_OFERTA = request.POST.get('id_oferta')
        ID_PROVEEDOR = request.POST.get('id_proveedor')
        NOMBRE_PROVEEDOR = request.POST.get('nombre_proveedor')
        APELLIDO_PROVEEDOR = request.POST.get('apellido_proveedor')
        EMAIL = request.POST.get('email')
        OFERTA = request.POST.get('oferta')
        FECHA = request.POST.get('fecha')
        EMPLEADO_RUT = request.POST.get('empleado_rut')
        salida = agregar_oferta(ID_OFERTA, ID_PROVEEDOR, NOMBRE_PROVEEDOR, APELLIDO_PROVEEDOR, EMAIL, OFERTA, FECHA, EMPLEADO_RUT)
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
            data['ofertas'] = listado_ofertas()
        else:
            data['mensaje'] = 'No se ha podido guardar'
    return render(request, 'subir_oferta.html', data)


def listado_ofertas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_OFERTAS',[out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def agregar_oferta(ID_OFERTA, ID_PROVEEDOR, NOMBRE_PROVEEDOR, APELLIDO_PROVEEDOR, EMAIL, OFERTA, FECHA, EMPLEADO_RUT):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_agregar_oferta',[ID_OFERTA, ID_PROVEEDOR, NOMBRE_PROVEEDOR, APELLIDO_PROVEEDOR, EMAIL, OFERTA, FECHA, EMPLEADO_RUT, salida])
    return salida.getvalue()



