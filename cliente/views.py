from django.shortcuts import render
from django.db import connection
import cx_Oracle
# Create your views here.

def histcliente(request):
    data = {
        'ordenes':historial(),
    }
    if request.method=='POST':
        email = request.POST.get('email')

    return render(request, "perfil.html", data)

def modificar_datos(request):
    return render(request, 'modificar_datos.html')

def listar_ciudad():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_CIUDAD", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila) 
    return lista


def historial(email):
	django_cursor = connection.cursor()
	cursor = django_cursor.connection.cursor()
	out_cur =django_cursor.connection.cursor()

	cursor.callproc("LISTAR_HISTORIAL", [email, out_cur])

	lista =[]
	for fila in out_cur:
		lista.append(fila)
	return lista