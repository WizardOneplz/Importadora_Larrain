from django import contrib
from django.shortcuts import render, redirect
from django.db import connection
from core.models import AuthGroup, Cliente, CuentaCliente, Rol
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
        salida = agregar_cliente(rut, nombre, ap_paterno, ap_materno, genero, telefono, email, direccion, ciudad, clave)
        if salida==1:
            data['MensajeRegistroCorrecto'] = 'Cliente Registrado Correctamente'
        else:
            data['MensajeRegistroError'] = 'No se ha podido registrar al Cliente'
    return render(request, 'registro.html' , data)

def agregar_cliente(rut,nombre,ap_paterno,ap_materno,genero,telefono,email,direccion,ciudad,clave):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('AGREGAR_CLIENTE',[rut, nombre, ap_paterno, ap_materno, genero, telefono, email, direccion, ciudad, clave, salida])
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
            return render(request, 'home.html' ,{ "cliente":Email})
        except CuentaCliente.DoesNotExist as e:
            messages.add_message(request=request, level=messages.ERROR, message="Correo o contraseña no coinciden.")
            return redirect('/')

def cerrarsesion(request):
    try:
        del request.session['email']
    except:
        return render(request, 'home.html')
    return render(request, 'home.html')

def modificar_cliente(request, cliente_rut):
    data={
        'cliente' : Cliente.objects.get(rut=cliente_rut),
        'cuentacliente': CuentaCliente.objects.get(cliente_rut=cliente_rut),
        'CIUDAD':listar_ciudad() 
    }
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

def cambclave (request):

    email = request.POST.get('email')
    rut = request.POST.get('rut')

    cuentacliente= CuentaCliente.objects.get(email=email)  
    cliente = Cliente.objects.get(rut=rut)
    contraseña2 = request.POST.get('nuevacontraseña')
    cuentacliente.clave = contraseña2
    cliente.clave =contraseña2 
    cuentacliente.save()
    cliente.save()
    return render(request,'home.html')
        
            


