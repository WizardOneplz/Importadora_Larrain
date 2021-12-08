from django.db import connection
from bodeguero.views import listar_productos
from django.shortcuts import redirect, render, get_object_or_404
from core.models import OrdenCompra
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
from cart.Carrito import Carrito
import base64
import cx_Oracle

# Create your views here.
def home(request):
    cart = Carrito(request)
    cart_product_form = CartAddProductForm()
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
        'page_obj': page_obj,
        'cart_product_form':cart_product_form,
        'cart':cart
    }
    return render(request, 'home.html', data)


def store(request):
    cart = Carrito(request)
    cart_product_form = CartAddProductForm()
    datos_productos = listar_productos()
    arreglo = []

    for i in datos_productos:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo.append(data)

    paginator = Paginator(arreglo, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'productos':arreglo,
        'page_obj': page_obj,
        'cart_product_form':cart_product_form,
        'cart':cart
    }

    return render(request, 'store.html', data)

def oferta(request):
    cart = Carrito(request)
    cart_product_form = CartAddProductForm()
    datos_productos = listado_oferta()
    arreglo = []

    for i in datos_productos:
        data = {
            'data':i,   
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo.append(data)

    paginator = Paginator(arreglo, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'productos':arreglo,
        'page_obj': page_obj,
        'cart_product_form':cart_product_form,
        'cart':cart
    }
    return render(request, 'oferta.html', data)


def producto(request, pk):
    cart = Carrito(request)
    datos_productos = listado_productos(id_pro = pk)
    valoraciones = listado_valoracion(id_producto=pk)
    cart_product_form = CartAddProductForm()
    
    arreglo = []
    for i in datos_productos:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo.append(data)
        
    data = {
        'productos': arreglo,
        'cart':cart,
        'cart_product_form':cart_product_form,
        'lista_valoraciones':valoraciones
    }
    
    if request.method== 'POST':
        valoracion = request.POST.get('valoracion')
        id_producto = request.POST.get('id_producto')
        comentario = request.POST.get('comentario')
        email = request.POST.get('email')
        salida = agregar_valoracion(valoracion, id_producto, comentario, email)     
        
    return render(request, 'producto.html', data)      

def seguimiento(request):
    cart = Carrito(request)
    return render(request,'seguimiento.html', {'cart':cart})

def mostrarinfo(request):
    try:
        id_orden = request.POST.get('id_orden')
        ordencompra = OrdenCompra.objects.get(id_orden=id_orden)
        return render(request,'info_orden.html', {"orden": ordencompra})
    except:
        return redirect('/seguimiento')

def agregar_valoracion(valoracion,id_producto, comentario, email):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_VALORACION',[valoracion, id_producto, comentario, email, salida])
    return salida.getvalue()


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

def listado_valoracion(id_producto):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("LISTAR_VALORACION", [id_producto, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
        
    return lista


def listado_oferta():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_PRODUCTO_OFERTA", [out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(fila)
    return lista

def search(request):
    q = request.GET['q']
    data = Producto.objects.filter(nombre_producto__icontains=q).order_by('-id_producto')
    
    paginator = Paginator(data, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render (request, 'search.html', {'data':data, 'page_obj':page_obj})
        

