from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from core.models import EstadoSolicitud, Producto, OrdenCompra, SolicitudProductos, Marca, Categoria
import cx_Oracle

# Create your views here.

def mantenedor_marca(request):
    data = {
        'productos':listar_productos(),
        'listapedidos':listar_pedidos(),
        'productoslistados': Producto.objects.all(),
        'pedidoslistados': OrdenCompra.objects.all(),
        'solicitudes': SolicitudProductos.objects.all(),
        'marcas': Marca.objects.all(),
        'categorias': Categoria.objects.all(),
        'solcitud':listar_solicitudes()
    }

    #agregar_marca(4,'Genius')

    if request.method== 'POST':
        nombre_marca = request.POST.get('nombre_marca')
        salida = agregar_marca(nombre_marca)
        if salida==1:
            data['MensajeMarca'] = 'Marca registrada correctamente'
        else:
            data['MensajeMarca'] = 'No se ha podido registrar la marca'
            data['MensajeProducto'] = 'Producto registrado correctamente'

    return render(request, 'mantenedor_marca.html', data)

def mantenedor_categorias(request):
    data = {
        'marcas':Marca.objects.all(),
        'categorias': Categoria.objects.all(),
        'productos':listar_productos(),
        'listapedidos':listar_pedidos(),
        'productoslistados': Producto.objects.all(),
        'pedidoslistados': OrdenCompra.objects.all(),
        'solicitudes': SolicitudProductos.objects.all(),
        'solcitud':listar_solicitudes()
    }

    if request.method== 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        salida = agregar_categoria(nombre_categoria)
        if salida==1:
            data['MensajeCategoria'] = 'Categoria registrada correctamente'
        else:
            data['MensajeCategoria'] = 'No se ha podido registrar la categoria'  


    return render(request, 'mantenedor_categorias.html', data)

def mantenedor_productos(request):
    data = {
        'marcas':Marca.objects.all(),
        'categorias': Categoria.objects.all(),
        'productos':listar_productos(),
        'listapedidos':listar_pedidos(),
        'productoslistados': Producto.objects.all(),
        'pedidoslistados': OrdenCompra.objects.all(),
        'solicitudes': SolicitudProductos.objects.all(),
        'solcitud':listar_solicitudes()
    }

    return render(request, 'mantenedor_productos.html', data)             

def listar_productos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def listar_pedidos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PEDIDOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def listar_solicitudes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_SOLICITUDES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def agregar_marca(nombre_marca):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_MARCA',[nombre_marca, salida])
    return salida.getvalue()

def agregar_categoria(nombre_categoria):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CATEGORIA',[nombre_categoria, salida])
    return salida.getvalue()

def cargar_producto(request):
    nombre_producto = request.POST.get('nombre_producto')
    precio = request.POST.get('precio')
    stock = request.POST.get('stock')
    oferta = request.POST.get('oferta')
    porcentaje = request.POST.get('p_oferta')
    id_marca = request.POST.get('id_marca')
    id_categoria = request.POST.get('id_categoria')
    imagen = request.FILES['imagen'].read()
    salida = agregar_producto(nombre_producto, precio, stock, oferta, porcentaje, id_marca, id_categoria, imagen)

    return redirect('/mantenedor_productos')

def agregar_producto(nombre_producto, precio, stock, oferta, porcentaje, id_marca, id_categoria, imagen):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PRODUCTO',[nombre_producto, precio, stock, oferta, porcentaje, id_marca, id_categoria, imagen, salida])
    return salida.getvalue()

def eliminar_producto(request, id_producto):
    producto = Producto.objects.get(id_producto=id_producto)
    producto.delete()

    return redirect('/mantenedor_productos')

def modificar_producto(request, id_producto):

    producto = Producto.objects.get(id_producto=id_producto)

    return render(request, "modificar_producto.html", {"productos": producto})

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

def modificar_producto(request, id_producto):
    
    producto = Producto.objects.get(id_producto=id_producto)

    return render(request, "modificar_producto.html", {"productos": producto})


def modificar_solicitud(request, id_solicitud):
    
    data = {
          'solicitudes': SolicitudProductos.objects.get(id_solicitud=id_solicitud),
          'solicitud': listar_solicitudes()  
    }

    return render(request, "modificar_solicitud.html", data)

def editar_solicitud(request):

    id_solicitud = request.POST.get('id_solicitud')  
    nombre_producto = request.POST.get('nombre_producto')
    observacion = request.POST.get('observacion')
    estado = request.POST.get('id_estado')

    solicitud = SolicitudProductos.objects.get(id_solicitud=id_solicitud)
    solicitud.id_solicitud = id_solicitud
    solicitud.nombre_producto = nombre_producto
    solicitud.observacion = observacion
    solicitud.estado_solicitud_id_estado = EstadoSolicitud.objects.get(id_estado = estado)
    solicitud.save() 
    
    return redirect('/mantenedor_productos')

def eliminar_marca(request, id_marca):
    marca = Marca.objects.get(id_marca=id_marca)
    marca.delete()

    return redirect('/mantenedor_marca')

def modificar_marca(request, id_marca):
    
    marca = Marca.objects.get(id_marca=id_marca)

    return render(request, "modificar_marca.html", {"marca": marca})

def editar_marca(request):
    
    id_marca = request.POST.get('id_marca')  
    nombre_marca = request.POST.get('nombre_marca')

    marca = Marca.objects.get(id_marca=id_marca)
    marca.id_marca = id_marca
    marca.nombre_marca = nombre_marca
    marca.save() 
    
    return redirect('/mantenedor_marca')

def eliminar_categoria(request, id_categoria):
    categoria = Categoria.objects.get(id_categoria=id_categoria)
    categoria.delete()

    return redirect('/mantenedor_categorias')

def modificar_categoria(request, id_categoria):
    
    categoria = Categoria.objects.get(id_categoria=id_categoria)

    return render(request, "modificar_categoria.html", {"categoria": categoria})

def editar_categoria(request):
    
    id_categoria = request.POST.get('id_categoria')  
    nombre_categoria = request.POST.get('nombre_categoria')

    categoria = Categoria.objects.get(id_categoria=id_categoria)
    categoria.id_categoria = id_categoria
    categoria.nombre_categoria = nombre_categoria
    categoria.save() 
    
    return redirect('/mantenedor_categorias')