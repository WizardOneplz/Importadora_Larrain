from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from core.models import Producto
import cx_Oracle

# Create your views here.

def mantenedor_productos(request):
    data = {
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
        'productos':listar_productos(),
        'productoslistados': Producto.objects.all()
    }

    #agregar_marca(4,'Genius')

    if request.method== 'POST':
        id_producto = request.POST.get('id')  
        nombre_producto = request.POST.get('nombre_producto')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        oferta = request.POST.get('oferta')
        porcentaje = request.POST.get('p_oferta')
        id_marca = request.POST.get('id_marca')
        id_categoria = request.POST.get('id_categoria')
        imagen = request.FILES['imagen'].read()
        salida = agregar_producto(id_producto, nombre_producto, precio, stock, oferta, porcentaje, id_marca, id_categoria, imagen)
        if salida==1:
            data['mensaje'] = 'Producto registrado correctamente'
        else:
            data['mensaje'] = 'No se ha podido registrar el producto'

    if request.method== 'POST':
        id = request.POST.get('id')
        nombre_marca = request.POST.get('nombre_marca')
        salida = agregar_marca(id, nombre_marca)
        if salida==1:
            data['mensaje'] = 'Marca registrada correctamente'
            data['marcas'] = listar_marcas()
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


    return render(request, 'mantenedor_productos.html', data)       

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

def listar_productos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

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

def agregar_producto(id_producto, nombre_producto, precio, stock, oferta, porcentaje, id_marca, id_categoria, imagen):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PRODUCTO',[id_producto, nombre_producto, precio, stock, oferta, porcentaje, id_marca, id_categoria, imagen, salida])
    return salida.getvalue()

def eliminar_producto(request, id_producto):
    producto = Producto.objects.get(id_producto=id_producto)
    producto.delete()

    return redirect('/mantenedor_productos')

def modificar_producto(request, id_producto):
    data = {
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
        'productos':listar_productos(),
        'productoslistados': Producto.objects.all()
    }

    producto = Producto.objects.get(id_producto=id_producto)

    return render(request, "modificar_producto.html", data)

def editar_producto(request):

    id_producto = request.POST.get('id')  
    nombre_producto = request.POST.get('nombre_producto')
    stock = request.POST.get('stock')

    producto = Producto.objects.get(id_producto=id_producto)
    producto.id_producto = id_producto
    producto.nombre_producto = nombre_producto
    producto.stock = stock
    producto.save() 
    
    return redirect('/mantenedor_productos')
