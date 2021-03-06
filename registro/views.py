from django import contrib
from django.shortcuts import render, redirect
from django.db import connection
from cliente.views import historial
from core.models import AuthGroup, Cliente, CuentaCliente, Rol,OrdenCompra
from django.contrib import messages
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
            data['MensajeRegistroCorrecto'] = 'Cliente Registrado Correctamente'
        else:
            data['MensajeRegistroError'] = 'No se ha podido registrar al Cliente'
    return render(request, 'registro.html' , data)

def agregar_cliente(rut,nombre,ap_paterno,ap_materno,genero,telefono,email,direccion, clave, ciudad):
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
            clave=request.POST['contrase??a'])
            request.session['email']=Email.email
            return render(request, 'home.html' ,{ "cliente":Email})
        except CuentaCliente.DoesNotExist as e:
            messages.add_message(request=request, level=messages.ERROR, message="Correo o contrase??a no coinciden.")
            return redirect('/')

def cerrarsesion(request):
    try:
        del request.session['email']
    except:
        return redirect('/')
    return redirect('/')

def modificar_cliente(request, cliente_rut): 
    cliente = Cliente.objects.get(rut=cliente_rut)
    compras = historial(email= cliente.email)
    data={
        'cliente' : Cliente.objects.get(rut=cliente_rut),
        'cuentacliente': CuentaCliente.objects.get(cliente_rut=cliente_rut),
        'CIUDAD':listar_ciudad(), 
        'listacompras':compras,
    }
    cuentacliente = CuentaCliente.objects.get(cliente_rut=cliente_rut)
    if request.method == 'POST':
        try:
            if cliente.clave != request.POST.get('clave'):#Al equivocarse en la clave actual, el sistema no permite seguir con el proceso.
                messages.add_message(request=request, level=messages.ERROR, message="Su contrase??a actual no es correcta.")
                return render(request, "perfil.html",data)
            elif cliente.clave == request.POST.get('clave'):
                contrase??a1 = request.POST.get('nuevacontrase??a')
                contrase??a2 = request.POST.get('repetircontrase??a1')
                if contrase??a2 == contrase??a1:
                    cuentacliente.clave = contrase??a2
                    cliente.clave =contrase??a2 
                    cuentacliente.save()
                    cliente.save()
                    messages.add_message(request=request, level=messages.SUCCESS, message="Contrase??a cambiada con ??xito.")
                    return render(request, "perfil.html",data)
                if contrase??a2 != contrase??a1: #Si las claves son distintas, no guarda y me indica el error.
                    messages.add_message(request=request, level=messages.ERROR, message="Las contrase??as nuevas no coinciden.")
                    return render(request, "perfil.html",data)
            else:
                 messages.add_message(request=request, level=messages.ERROR, message="Ha ocurrido un error inesperado, porfavor intente nuevamente.")
                 return render(request, "perfil.html",data) 
        except:
            messages.add_message(request=request, level=messages.ERROR, message="Ha ocurrido un error inesperado, porfavor intente nuevamente.")
            return render(request, "perfil.html",data)
    return render(request, "perfil.html", data)


def perfil(request):

    rut = request.POST.get('rut')
    nombre = request.POST.get('nombre')
    ap_paterno = request.POST.get('ap_paterno')
    ap_materno = request.POST.get('ap_materno')
    genero = request.POST.get('genero')
    telefono = request.POST.get('telefono')
    email = request.POST.get('email')
    direccion = request.POST.get('Direccion')
    ciudad = request.POST.get('ciudad')
     
    cliente = Cliente.objects.get(rut=rut)
    cliente.rut = rut
    cliente.nombre = nombre
    cliente.apellido_paterno = ap_paterno
    cliente.apellido_materno = ap_materno
    cliente.genero = genero
    cliente.telefono = telefono
    cliente.email = email
    cliente.direccion = direccion
    cliente.ciudad = ciudad
    cliente.save()
    return redirect('/')

##def cambclave (request):
    
        ##cuentacliente= CuentaCliente.objects.get(email=email)  
        ##cliente = Cliente.objects.get(rut=rut)
        ##contrase??a2 = request.POST.get('nuevacontrase??a')
        ##cuentacliente.clave = contrase??a2
        ##cliente.clave =contrase??a2 
        ##cuentacliente.save()
        ##cliente.save()
        ##return render(request,'home.html')
        
