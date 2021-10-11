from django.shortcuts import render

# Create your views here.

def subir_oferta(request):
    return render(request, 'subir_oferta.html')