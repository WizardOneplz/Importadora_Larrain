from core.models import Producto
from decimal import Decimal
from django.conf import settings

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get(settings.CART_SESSION_ID)
        if not carrito:
            carrito = self.session[settings.CART_SESSION_ID] = {}
        self.carrito = carrito
    
    def __iter__(self):
        producto_ids = self.carrito.keys()
        productos = Producto.objects.filter(id_producto__in=producto_ids)
        carrito = self.carrito.copy()
        for producto in productos:
            carrito[str(producto.id_producto)]['id_producto'] = producto
        for item in carrito.values():
            item['precio'] = int(item['precio'])
            item['precio_total'] = item['precio'] * item['cantidad']
            yield item
    
    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def agregar(self, producto, quantity = 1, override_quantity= False):
        id = str(producto.id_producto)
        if id not in self.carrito:
            self.carrito[id] = {'cantidad':0, 'precio': str(producto.precio)}
        if override_quantity:
            self.carrito[id]['cantidad'] = quantity
        else:
            self.carrito[id]['cantidad'] += quantity
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session.modified = True

    def eliminar(self, productos):
        id = str(productos.id_producto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, productos):
        id = str(productos.id_producto)
        if id in self.carrito.keys():
            self.carrito[id]['cantidad'] -= 1
            self.carrito[id]['precio'] -= productos.precio
            if self.carrito[id]['cantidad'] <= 0:
                self.eliminar(productos)
            self.guardar_carrito()

    def limpiar(self):
        del self.session[settings.CART_SESSION_ID]
        self.guardar_carrito()
        
    def get_total_price(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())
    
    def get_cantidad(self):
        return sum(item['cantidad'] for item in self.carrito.values())

