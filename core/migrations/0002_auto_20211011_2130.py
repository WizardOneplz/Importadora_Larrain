# Generated by Django 3.2.8 on 2021-10-12 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bodega',
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
        migrations.DeleteModel(
            name='Ciudad',
        ),
        migrations.DeleteModel(
            name='Cliente',
        ),
        migrations.DeleteModel(
            name='CuentaCliente',
        ),
        migrations.DeleteModel(
            name='CuentaEmpleado',
        ),
        migrations.DeleteModel(
            name='DetalleOrden',
        ),
        migrations.DeleteModel(
            name='Empleado',
        ),
        migrations.DeleteModel(
            name='EstadoPago',
        ),
        migrations.DeleteModel(
            name='EstadoPedido',
        ),
        migrations.DeleteModel(
            name='Estanteria',
        ),
        migrations.DeleteModel(
            name='Marca',
        ),
        migrations.DeleteModel(
            name='Oferta',
        ),
        migrations.DeleteModel(
            name='Pasillo',
        ),
        migrations.DeleteModel(
            name='Producto',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.DeleteModel(
            name='Rol',
        ),
        migrations.DeleteModel(
            name='SolicitudProductos',
        ),
        migrations.DeleteModel(
            name='TipoOrden',
        ),
        migrations.DeleteModel(
            name='TipoPago',
        ),
        migrations.DeleteModel(
            name='Valoracion',
        ),
        migrations.DeleteModel(
            name='OrdenCompra',
        ),
        
    ]