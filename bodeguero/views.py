from django.shortcuts import render

# Create your views here.

def mantenedor_productos(request):
    return render(request, 'mantenedor_productos.html')