from typing import List
from django.db import connection
from django.shortcuts import redirect, render, get_object_or_404
from bodeguero.views import agregar_producto, listar_productos

from django.core.paginator import Paginator

from core.models import Producto, Marca, Categoria
from django.core.files.base import ContentFile
import base64

# Create your views here.
def home(request):
    datos_productos = listar_productos()
    arreglo = []

    for i in datos_productos:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo.append(data)

    paginator = Paginator(arreglo, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'productos':arreglo,
        'page_obj': page_obj
    }
    return render(request, 'home.html', data)


def carrito(request):
    productos = Producto.objects.all()
    return render(request, 'cart.html', {'productos': productos})


def store(request):
    datos_productos = listar_productos()
    arreglo = []

    for i in datos_productos:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo.append(data)

    paginator = Paginator(arreglo, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'productos':arreglo,
        'page_obj': page_obj
    }

    return render(request, 'store.html', {'page_obj':page_obj})


def producto(request, pk):

    datos_productos = listado_productos(id_pro = pk)
    productos = Producto.objects.filter(pk=pk)
    
    arreglo = []
    for i in datos_productos:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo.append(data)
    data = {
        'productos': arreglo,
    }
    return render(request, 'producto.html', data)


def listado_productos(id_pro):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_MOSTRAR_PRODUCTO", [out_cur, id_pro])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(fila)
    return lista