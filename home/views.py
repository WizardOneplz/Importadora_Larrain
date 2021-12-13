from django.db import connection
from bodeguero.views import listar_productos
from django.shortcuts import redirect, render, get_object_or_404
from core.models import Categoria, DetalleOrden, OrdenCompra, Producto, Marca, CuentaEmpleado
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
from cart.Carrito import Carrito
from django.contrib import messages
import base64
import cx_Oracle

# Create your views here.
def home(request):
    cart = Carrito(request)
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    cart_product_form = CartAddProductForm()

    datos_valoracion = listado_valoraciontotal()
    datos_productos = listado_oferta()
    datos_nuevos = listado_novedades()

    arreglo = []
    arreglo_novedades = []
    arreglo_valoracion = []

    for i in datos_productos:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo.append(data)
    
    for i in datos_valoracion:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo_valoracion.append(data)
    
    for i in datos_nuevos:
        data = {
            'data':i,
            'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
        }
        arreglo_novedades.append(data)

    paginator_val = Paginator(arreglo_valoracion, 4)
    paginator = Paginator(arreglo, 4)
    paginator_nov = Paginator(arreglo_novedades, 4)
    page_number = request.GET.get('page')
    page_obj__= paginator_nov.get_page(page_number)
    page_obj_ = paginator_val.get_page(page_number)
    page_obj = paginator.get_page(page_number)

    data = {
        'valoracion':arreglo_valoracion,
        'productos':arreglo,
        'page_obj': page_obj,
        'page_obj_': page_obj_,
        'page_obj__': page_obj__,
        'cart_product_form':cart_product_form,
        'cart':cart,
        'categorias':categorias,
        'marcas':marcas,
    }
    
    if request.method =='POST':
        try: 
            Usuario=CuentaEmpleado.objects.get(usuario = request.POST['empleado'],
            clave=request.POST['clave'])
            request.session['usuario']=Usuario.usuario 
            if Usuario.rol == 1 :
                return render(request, 'agregar_empleado.html',{"empleado":Usuario} )
            elif Usuario.rol == 3 :
                return render(request,'subir_oferta.html' ,{"empleado":Usuario})
            elif Usuario.rol == 4 :
                return render(request,'registro.html',{"empleado":Usuario})
            elif Usuario.rol == 5 :
                return render(request,'mantenedor_marca.html',{"empleado":Usuario})
        except CuentaEmpleado.DoesNotExist as e:
            messages.add_message(request=request, level=messages.ERROR, message="Correo o contraseña no coinciden.")
            return redirect('/')
    
    return render(request, 'home.html', data)

def store(request):
    cart = Carrito(request)
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
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
        'cart':cart,
        'categorias':categorias,
        'marcas':marcas,
    }

    return render(request, 'store.html', data)

def oferta(request):
    cart = Carrito(request)
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
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
        'cart':cart,
        'categorias':categorias,
        'marcas':marcas,
    }
    return render(request, 'oferta.html', data)

def categoria(request, id_categoria):
    cart = Carrito(request)
    cart_product_form = CartAddProductForm()
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    categoriass = Categoria.objects.get(id_categoria = id_categoria)
    datos_productos = listado_categoria(id_cat = id_categoria)
    
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
        'cart':cart,
        'categorias':categorias,
        'categoriass':categoriass,
        'marcas':marcas,
    }
    return render(request, 'categoria.html', data)

def marca(request, id_marca):
    cart = Carrito(request)
    cart_product_form = CartAddProductForm()
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    cart_product_form = CartAddProductForm()
    marcass = Marca.objects.get(id_marca = id_marca)
    datos_productos = listado_marca(id_mar = id_marca)
    
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
        'cart':cart,
        'categorias':categorias,
        'marcass':marcass,
        'marcas':marcas,
    }
    return render(request, 'marca.html', data)

def producto(request, pk):
    cart = Carrito(request)
    productoss = Producto.objects.get(id_producto = pk)
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
        'productoss':productoss,
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
        if salida==1:
                data['MensajeCategoriaCorrecto'] = 'Categoria registrada correctamente'
                data['lista_valoraciones'] = listado_valoracion(id_producto=pk)
        else:
            data['MensajeCategoriaError'] = 'El nombre de la categoria ya esta siendo utilizado'       
        
    return render(request, 'producto.html', data)      

def search(request):
    q = request.GET['q']
    data = Producto.objects.filter(nombre_producto__icontains=q).order_by('-id_producto')
    cart_product_form = CartAddProductForm()
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    arreglo = []

    if data.exists():
        for it in data:
            datos_productos = listado_productos(id_pro = it.id_producto)

        for i in datos_productos:
            data = {
                'data':i,
                'imagen':str(base64.b64encode(i[6].read()), 'utf-8')
            }
            arreglo.append(data)

    paginator = Paginator(arreglo, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render (request, 'search.html', {'data':data, 'page_obj':page_obj, 'cart_product_form':cart_product_form, 'productos':arreglo, 'categorias':categorias, 'marcas':marcas})

def seguimiento(request):
    cart = Carrito(request)
    return render(request,'seguimiento.html', {'cart':cart})

def mostrarinfo(request):
    try:
        id_orden = request.POST.get('id_orden')
        data={
            "orden": OrdenCompra.objects.get(id_orden=id_orden),
            "productos":DetalleOrden.objects.filter(orden_compra_id_orden=id_orden)   
        }
        return render(request,'info_orden.html', data)
    except OrdenCompra.DoesNotExist as e:
        messages.add_message(request=request, level=messages.ERROR, message="No se ha encontrado la orden solicitada.")
        return redirect('/seguimiento')

def agregar_valoracion(valoracion,id_producto, comentario, email):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_VALORACION',[valoracion, id_producto, comentario, email, salida])
    return salida.getvalue()


def listado_novedades():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_PRODUCTO_NUEVOS", [out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(fila)
    return lista


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


def listado_valoraciontotal():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_PRODUCTO_VALORACION", [out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(fila)
    return lista

def listado_categoria(id_cat):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_PRODUCTO_CATEGORIA", [out_cur, id_cat])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(fila)
    return lista

def listado_marca(id_mar):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc("SP_PRODUCTO_MARCA", [out_cur, id_mar])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(fila)
    return lista


        

