from django.shortcuts import render, redirect
from django.db import connection
from core.models import Empleado,CuentaEmpleado, Rol, Estanteria, Bodega, Pasillo
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
        'listado_bodega':Bodega.objects.all(),
        'bodega':listado_bodega(),
        'pasillo':listado_pasillo(),
        'listar_pasillo':Pasillo.objects.all(),
        'estanteria':listado_estanteria(),
        'listar_estanteria':Estanteria.objects.all(),
        
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
            data['MensajeEmpleadoCorrecto'] = 'Empleado registrado correctamente.'
            data['empleados'] = listado_empleados()
        else:
            data['MensajeEmpleadoError'] = 'Rut o Correo ya registrado.' 

    return render(request,'agregar_empleado.html',data)

#BODEGA
def mantenedor_bodega(request):
    data = {
        'cargos':listar_cargos(),
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
        'productos':listar_productos(),
        'cliente':listado_clientes(),
        'empleados':listado_empleados(),
        'listar_empleados':Empleado.objects.all(),
        'listado_bodega':Bodega.objects.all(),
        'bodega':listado_bodega(),
        'pasillo':listado_pasillo(),
        'listar_pasillo':Pasillo.objects.all(),
        'estanteria':listado_estanteria(),
        'listar_estanteria':Estanteria.objects.all(),
        
    } 

#AGREGAR BODEGA
    if request.method== 'POST':
        cant_pasillos = request.POST.get('cant_pasillos')
        direccion = request.POST.get('direccion')

        salida = agregar_bodega(cant_pasillos,direccion)
        if salida==1:
            data['MensajeBodegaCorrecto'] = 'Bodega registrada correctamente.'
            data['bodega'] = listado_bodega()
        else:
            data['MensajeBodegaError'] = 'Direccion de bodega ya registrado.' 

    return render(request,'mantenedor_bodega.html',data)

#PASILLO
def mantenedor_pasillo(request):
    data = {
        'cargos':listar_cargos(),
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
        'productos':listar_productos(),
        'cliente':listado_clientes(),
        'empleados':listado_empleados(),
        'listar_empleados':Empleado.objects.all(),
        'listado_bodega':Bodega.objects.all(),
        'bodega':listado_bodega(),
        'pasillo':listado_pasillo(),
        'listar_pasillo':Pasillo.objects.all(),
        'estanteria':listado_estanteria(),
        'listar_estanteria':Estanteria.objects.all(),
        
    } 

#AGREGAR PASILLO
    if request.method== 'POST':
        cant_estanterias = request.POST.get('cant_estanterias')
        id_bodega = request.POST.get('id_bodega')

        salida = agregar_pasillo(cant_estanterias,id_bodega)
        if salida==1:
            data['MensajePasilloCorrecto'] = 'Pasillo registrado correctamente.'
            data['pasillo'] = listado_pasillo()
        

    return render(request,'mantenedor_pasillo.html',data)


#ESTANTERIA
def mantenedor_estanteria(request):
    data = {
        'cargos':listar_cargos(),
        'marcas':listar_marcas(),
        'categorias':listar_categorias(),
        'productos':listar_productos(),
        'cliente':listado_clientes(),
        'empleados':listado_empleados(),
        'listar_empleados':Empleado.objects.all(),
        'listado_bodega':Bodega.objects.all(),
        'bodega':listado_bodega(),
        'pasillo':listado_pasillo(),
        'listar_pasillo':Pasillo.objects.all(),
        'estanteria':listado_estanteria(),
        'listar_estanteria':Estanteria.objects.all(),
        
    } 

#AGREGAR ESTANTERIA
    if request.method== 'POST':
        cant_estanterias = request.POST.get('cant_estanterias')
        id_bodega = request.POST.get('id_bodega')

        salida = agregar_pasillo(cant_estanterias,id_bodega)
        if salida==1:
            data['MensajeEstanteriaCorrecto'] = 'Estantería registrada correctamente.'
            data['pasillo'] = listado_pasillo()

    return render(request,'mantenedor_estanteria.html',data)

#METODOS


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

def eliminar_bodega(request, id_bodega):
    data = {}
    try:
        bodega = Bodega.objects.get(id_bodega=id_bodega)
        bodega.delete()
    except:
        return redirect('/agregar_empleado')
    
    return redirect('/agregar_empleado')


def modificar_bodega(request, id_bodega):
    bodega = Bodega.objects.get(id_bodega=id_bodega)
    
    return render(request, "modificar_bodega.html",{"bodegas":bodega})

def editar_bodega(request):
    
    id_bodega = request.POST.get('id_bodega')
    num_pasillo = request.POST.get('cant_pasillos')
    direccion = request.POST.get('direccion')
   
    bodega = Bodega.objects.get(id_bodega=id_bodega)
    bodega.id_bodega = id_bodega
    bodega.num_pasillo = num_pasillo
    bodega.direccion = direccion
    bodega.save()

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

def eliminar_pasillo(request, id_pasillo):
    try:
        pasillo = Pasillo.objects.get(id_pasillo=id_pasillo)
        pasillo.delete()
    except:
        estanteria = Estanteria.objects.get(pasillo_id_pasillo=id_pasillo)
        estanteria.delete()
        pasillo = Pasillo.objects.get(id_pasillo=id_pasillo)
        pasillo.delete()
    
    data={
        'pasillo':listado_pasillo()
    }

    return redirect('/agregar_empleado',data)

#ESTANTERIA

def agregar_estanteria(capacidad,id_pasillo,id_producto):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('ADM_AGREGAR_ESTANTERIA',[capacidad,id_pasillo,id_producto, salida])
    return salida.getvalue()

def listado_estanteria():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_ESTANTERIA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def eliminar_estanteria(request, id_estanteria):
    estanteria = Estanteria.objects.get(id_estanteria=id_estanteria)
    estanteria.delete()
    return redirect('/agregar_empleado')

#login 

def logemp(request):
    if request.method =='POST':
        try:
            Usuario=CuentaEmpleado.objects.get(usuario = request.POST['empleado'],
            clave =request.POST['clave'])
            request.session['usuario']=Usuario.usuario 
            #OBTENER EL ROL
            if Usuario.rol_id_rol== 1:
                return render(request,'agregar_empleado.html')
            elif Usuario.rol_id_rol == 3:
                return render(request,'subir_oferta.html')
            elif Usuario.rol_id_rol == 4:
                return render(request,'registro.html')
            elif Usuario.rol_id_rol == 5:
                return render(request,'mantenedor_marca.html')
            else:
                return render(request,'home.html')      
        except:
            return render(request, 'mantenedor_productos.html')


def logout(request):
    try:
        del request.session['usuario']
    except:
        return render(request, 'home.html')
    return render(request, 'home.html')