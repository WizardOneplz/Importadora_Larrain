from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from core.models import EstadoSolicitud, Producto, OrdenCompra, SolicitudProductos
import cx_Oracle

# Create your views here.

def mantenedor_productos(request):
    data = {
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
        'productos':listar_productos(),
        'listapedidos':listar_pedidos(),
        'productoslistados': Producto.objects.all(),
        'pedidoslistados': OrdenCompra.objects.all(),
        'solicitudes': SolicitudProductos.objects.all(),
        'solcitud':listar_solicitudes()
    }

    #agregar_marca(4,'Genius')

    if request.method== 'POST':
        nombre_marca = request.POST.get('nombre_marca')
        salida = agregar_marca(nombre_marca)
        if salida==1:
            data['MensajeMarca'] = 'Marca registrada correctamente'
            data['marcas'] = listar_marcas()
        else:
            data['MensajeMarca'] = 'No se ha podido registrar la marca'
            data['MensajeProducto'] = 'Producto registrado correctamente'

    if request.method== 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        salida = agregar_categoria(nombre_categoria)
        if salida==1:
            data['MensajeCategoria'] = 'Categoria registrada correctamente'
            data['categorias'] = listar_categorias()
        else:
            data['MensajeCategoria'] = 'No se ha podido registrar la categoria'  


    return render(request, 'mantenedor_productos.html', data)

def mantenedor_categorias(request):
    data = {
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
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
            data['categorias'] = listar_categorias()
        else:
            data['MensajeCategoria'] = 'No se ha podido registrar la categoria'  


    return render(request, 'mantenedor_categorias.html', data)        

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
