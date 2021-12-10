from django.shortcuts import render
from .Carrito import Carrito
from .forms import CartAddProductForm, OrderCreateForm
from core.models import DetalleOrden, Producto, CuentaCliente
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
def cart(request):
    cart = Carrito(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
        'cantidad': item['cantidad'],
        'override': True})
    return render(request, 'cart.html', {'cart':cart})
 
def order_create(request):
    cart = Carrito(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.precio_total = cart.get_total_price()
            correo = request.POST.get('email')
            order.cuenta_cliente_email = CuentaCliente.objects.get(email=correo)
            order.save()
            for item in cart:
                DetalleOrden.objects.create(cantidad = item['cantidad'], precio = item['precio'],producto_id_producto=item['id_producto'], orden_id_orden=order)
            cart.limpiar()
            return render(request, 'created.html',{'order':order})
    else:
        form = OrderCreateForm()
    return render(request, 'create.html', {'cart': cart, 'form':form})

@require_POST
def agregar_carrito(request, id_producto):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id_producto=id_producto)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        carrito.agregar(producto=producto, quantity=cd['cantidad'], override_quantity=cd['override'])
    return redirect("/cart")

@require_POST
def eliminar_carrito(request, id_producto):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id_producto=id_producto)
    carrito.eliminar(producto)
    return redirect("/cart")

def restar_carrito(request, id_producto):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=id_producto)
    carrito.restar(producto)
    return redirect("/cart")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("/cart")