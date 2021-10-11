from django.contrib import admin
from .models import Bodega, Categoria, Ciudad, Cliente, CuentaCliente, CuentaEmpleado, DetalleOrden, Empleado, EstadoPago, EstadoPedido, Estanteria, Marca, Oferta, OrdenCompra, Pasillo, Producto, Region, Rol, SolicitudPresencial, SolicitudProductos, TipoOrden, TipoPago, Valoracion

# Register your models here.

admin.site.register(Bodega)
admin.site.register(Categoria)
admin.site.register(Ciudad)
admin.site.register(Cliente)
admin.site.register(CuentaCliente)
admin.site.register(CuentaEmpleado)
admin.site.register(DetalleOrden)
admin.site.register(Empleado)
admin.site.register(EstadoPago)
admin.site.register(EstadoPedido)
admin.site.register(Estanteria)
admin.site.register(Marca)
admin.site.register(Oferta)
admin.site.register(OrdenCompra)
admin.site.register(Pasillo)
admin.site.register(Producto)
admin.site.register(Region)
admin.site.register(Rol)
admin.site.register(SolicitudPresencial)
admin.site.register(SolicitudProductos)
admin.site.register(TipoOrden)
admin.site.register(TipoPago)
admin.site.register(Valoracion)


