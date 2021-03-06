from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import authenticate
from core.models import Empleado,CuentaEmpleado, Rol, Estanteria, Bodega, Pasillo
from django.contrib import messages
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
        'pasillos':listar_pasillos(),
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
        capacidad = request.POST.get('capacidad')
        id_pasillo = request.POST.get('id_pasillo')
        id_producto = request.POST.get('id_producto')

        salida = agregar_estanteria(capacidad,id_pasillo,id_producto)
        if salida==1:
            data['MensajeEstanteriaCorrecto'] = 'Estanter??a registrada correctamente.'
            data['pasillo'] = listado_estanteria()

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
    try:
        cuentaempleado = CuentaEmpleado.objects.get(empleado_rut=rut)
        cuentaempleado.delete()
        empleado = Empleado.objects.get(rut=rut)
        empleado.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Empleado eliminado con ??xito.")
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Imposible Eliminar, empleado se relaciona con otras tablas.")    
    return redirect('/logemp/agregar_empleado')

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
    messages.add_message(request=request, level=messages.SUCCESS, message="Empleado modificado con ??xito.")

    return redirect('/logemp/agregar_empleado')
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

def listar_pasillos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_PASILLO", [out_cur])

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
        messages.add_message(request=request, level=messages.SUCCESS, message="Bodega eliminada con ??xito.")
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Imposible eliminar bodega, para realizar esta accion debe eliminar los pasillos de la bodega.")
        return redirect('/logemp/mantenedor_bodega')
    
    return redirect('/logemp/mantenedor_bodega')


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
    messages.add_message(request=request, level=messages.SUCCESS, message="Bodega modificada con ??xito.")

    return redirect('/logemp/mantenedor_bodega')

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
        messages.add_message(request=request, level=messages.SUCCESS, message="Pasillo eliminado con ??xito.Las estanter??as asociadas tambien se eliminaron.")
        return redirect('/logemp/mantenedor_pasillo')
    except:
        estanteria = Estanteria.objects.filter(pasillo_id_pasillo=id_pasillo)
        estanteria.delete()
        pasillo = Pasillo.objects.get(id_pasillo=id_pasillo)
        pasillo.delete()
        return redirect('/logemp/mantenedor_pasillo')
    
    data={
        'pasillo':listado_pasillo()
    }

    return redirect('/mantenedor_pasillo',data)

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
    messages.add_message(request=request, level=messages.SUCCESS, message="Estanter??a eliminada con ??xito.")
    return redirect('/logemp/mantenedor_estanteria')

#login 

def logemp(request):
    
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
            messages.add_message(request=request, level=messages.ERROR, message="Correo o contrase??a no coinciden.")
            return redirect('/')


def logout(request):
    try:
        del request.session['usuario']
    except:
        return redirect('/')
    return redirect('/')

def modificar_perfil(request, empleado_rut):
    data={
        'empleado' : Empleado.objects.get(rut=empleado_rut),
        'cuentaempleado': CuentaEmpleado.objects.get(empleado_rut=empleado_rut)
    }
    empleado = CuentaEmpleado.objects.get(empleado_rut=empleado_rut)
    if request.method == 'POST':
        try:
            if empleado.clave != request.POST.get('clave'):#Al equivocarse en la clave actual, el sistema no permite seguir con el proceso.
                messages.add_message(request=request, level=messages.ERROR, message="Su contrase??a actual no es correcta.")
                return render(request, "perfil_empleado.html",data)
            elif empleado.clave == request.POST.get('clave'): #If para comprobar que la clave actual ingresada sea igual a la de la BD.
                contrase??a2 = request.POST.get('nuevacontrase??aem')
                contrase??a1 = request.POST.get('repetircontrase??a')
                if contrase??a1 == contrase??a2: #Luego de comprobar las claves, se verifica que la clave nueva sea correcta en ambos campos.
                    empleado.clave = contrase??a2
                    empleado.save()
                    messages.add_message(request=request, level=messages.SUCCESS, message="Contrase??a cambiada con ??xito.")
                    return render(request, "perfil_empleado.html",data)
                if contrase??a1 != contrase??a2: #Si las claves son distintas, no guarda y me indica el error.
                    messages.add_message(request=request, level=messages.ERROR, message="Las contrase??as nuevas no coinciden.")
                    return render(request, "perfil_empleado.html",data)
            else: 
                messages.add_message(request=request, level=messages.ERROR, message="Ha ocurrido un error inesperado, porfavor intente nuevamente.")
                return render(request, "perfil_empleado.html",data)

        except:
            messages.add_message(request=request, level=messages.ERROR, message="Ha ocurrido un error inesperado, porfavor intente nuevamente.")
            return render(request, "perfil_empleado.html",data)
    return render(request, "perfil_empleado.html", data)


def peremple(request):

    rut = request.POST.get('rut')
    nombre = request.POST.get('nombre')
    ap_paterno = request.POST.get('ap_paterno')
    ap_materno = request.POST.get('ap_materno')
    genero = request.POST.get('genero')
    telefono = request.POST.get('telefono')
    email = request.POST.get('email')
    direccion = request.POST.get('Direccion')
    ciudad = request.POST.get('ciudad')
     
    empleado = Empleado.objects.get(rut=rut)
    empleado.rut = rut
    empleado.nombre = nombre
    empleado.apellido_paterno = ap_paterno
    empleado.apellido_materno = ap_materno
    empleado.genero = genero
    empleado.telefono = telefono
    empleado.email = email
    empleado.direccion = direccion
    empleado.ciudad = ciudad
    empleado.save()
    return redirect('/')

##def claveemple (request):
  ##  empleado = CuentaEmpleado.objects.get(empleado_rut=request.POST.get('rut'))
    ##try:
      ##  if empleado.Clave == request.POST.get('clave'):
        ##    contrase??a2 = request.POST.get('nuevacontrase??aem')
         ##   if request.POST.get('repetircontrase??a ') == contrase??a2:
           ##     empleado.Clave = contrase??a2
             ##   empleado.save()
              ##  return render(request, "perfil_empleado.html")
            ##else:
              ##  return render(request, "registro.html")
      ##          messages.add_message(request=request, level=messages.SUCCESS, message="porfavor repetir la nueva claave .")
    ##except:
     ##   return render(request, "registro.html")
        ##messages.add_message(request=request, level=messages.SUCCESS, message="su contrase??a actual no es correcta.")