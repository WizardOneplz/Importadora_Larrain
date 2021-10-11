from django.shortcuts import render

# Create your views here.

def modificar_datos(request):
    return render(request, 'modificar_datos.html')

def listar_datos(request):
    return render(request, 'listar_datos.html')