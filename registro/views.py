from django.shortcuts import render
from django.db import connection
from core.models import Cliente, CuentaCliente, Rol
from django.contrib import messages
import getpass
import cx_Oracle

# Create your views here.

def registro(request):
    data = {
        'CIUDAD':listar_ciudad()  
    }
    if request.method== 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        ap_paterno = request.POST.get('ap_paterno')
        ap_materno = request.POST.get('ap_materno')
        genero = request.POST.get('genero')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('Direccion')
        ciudad = request.POST.get('ciudad')
        clave= request.POST.get('clave')
        salida = agregar_cliente(rut, nombre, ap_paterno, ap_materno, genero, telefono, email, direccion, clave, ciudad)
        if salida==1:
            data['mensaje'] = 'Cliente Registrado Correctamente'
        else:
            data['mensaje'] = 'No se ha podido registrar al Cliente'
    return render(request, 'registro.html' , data)

def agregar_cliente(rut,nombre,ap_paterno,ap_materno,genero,telefono,email,direccion,clave,ciudad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('AGREGAR_CLIENTE',[rut, nombre, ap_paterno, ap_materno, genero, telefono, email, direccion, clave, ciudad, salida])
    return salida.getvalue()

def listar_ciudad():
     
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_CIUDAD", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila) 
    return lista

    #login 


def login(request):
    if request.method=='POST':
        try:
            Email=CuentaCliente.objects.get(email = request.POST['correo'],
            clave=request.POST['contraseña'])
            request.session['email']=Email.email
            # para empleado 
            # IF (si la credencial y clave es correcta)
                #OBTENER EL ROL
                    #IF ROL == 'ADMINISTRADOR' O el numero de rol ej: 4
                        # href a agregar_empleado
                    #ELSE IF ROL == 'BODEGUERO' O el numero de rol ej: 3
                        #href a mantenedor_producto
                    #ELSE IF ROL == 'AGENTE' O el numero de rol ej: 2
                        #href a subir_oferta
                    #ELSE IF ROL == 'VENDEDOR' O el numero de rol ej: 1
                        #href a "por definir".
            return render(request, 'home.html')
        except CuentaCliente.DoesNotExist as e:
            messages.success(request,'nombre de usuario o clave no correcto')
    return render(request, 'login.html')

def cerrarsesion(request):
    try:
        del request.session['email']
    except:
        return render(request, 'home.html')
    return render(request, 'home.html')



