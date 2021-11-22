from django.shortcuts import redirect, render, get_object_or_404

from core.models import OrdenCompra, Producto, Marca, Categoria  

# Create your views here.

def home(request):
    productos = Producto.objects.filter()
    return render(request, 'home.html', {'productos':productos})

def carrito(request):
    productos = Producto.objects.all()
    return render(request, 'cart.html', {'productos': productos})

def store(request):
    productos = Producto.objects.all()
    return render(request, 'store.html', {'productos': productos})

def producto(request, pk):
    marcas = get_object_or_404(Marca)
    categorias = get_object_or_404(Categoria)
    productos = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto.html',{'productos': productos, 'marcas':marcas, 'categorias':categorias})

def seguimiento(request):
  
    return render(request,'seguimiento.html')


def mostrarinfo(request):
    
    id_orden = request.POST.get('id_orden')
    
    ordencompra = OrdenCompra.objects.get(id_orden=id_orden)
    
    return render(request,'info_orden.html', {"orden": ordencompra})
