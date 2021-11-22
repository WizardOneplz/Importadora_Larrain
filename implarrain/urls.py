"""implarrain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import *  #esto se debe hacer cada vez que se quiera importar una views de las otras APPS
from registro.views import *
from administrador.views import *
from bodeguero.views import *
from cliente.views import *
from agente.views import *

urlpatterns = [
    #TIENDA
    path('admin/', admin.site.urls),
    path('',home),
    path('carrito', carrito),
    path('store', store),
    path('producto/<int:pk>/', producto, name='producto'),
    path('seguimiento', seguimiento),
    path('mostrar_info/', mostrarinfo),
    #REGISTRO
    path('registro',registro),
    path('agregar_empleado',mantenedor_admin),
    path('login', login), 
    path('cerrarsesion',cerrarsesion),
    path('logemp',logemp),
    #ELIMINAR
    path('eliminar_empleado/<rut>',eliminar_empleado),
    path('eliminar_estanteria/<id_estanteria>',eliminar_estanteria),
    path('eliminar_pasillo/<id_pasillo>',eliminar_pasillo),
    path('eliminar_bodega/<id_bodega>',eliminar_bodega),
    path('eliminar_marca/<id_marca>',eliminar_marca),
    path('eliminar_categoria/<id_categoria>',eliminar_categoria),
    #MODIFICAR
    path('modificar_marca/<id_marca>',modificar_marca),
    path('editar_marca/',editar_marca),
    path('modificar_categoria/<id_categoria>',modificar_categoria),
    path('editar_categoria/',editar_categoria),
    path('modificar_bodega/<id_bodega>',modificar_bodega),
    path('editar_bodega/',editar_bodega),
    path('modificar_empleado/<rut>',modificar_empleado),
    path('editar_empleado/',editar_empleado),
    path('modificar_orden/<id_orden>',modificar_orden),
    path('editar_orden/',editar_orden),
    path('mantenedor_bodega',mantenedor_bodega),
    path('mantenedor_pasillo',mantenedor_pasillo),
    path('mantenedor_estanteria',mantenedor_estanteria),
    path('mantenedor_marca',mantenedor_marca),
    path('mantenedor_categorias',mantenedor_categorias),
    path('mantenedor_productos',mantenedor_productos),
    path('modificar_producto/<id_producto>',modificar_producto),
    path('modificar_solicitud/<id_solicitud>',modificar_solicitud),
    path('editar_producto/',editar_producto),
    path('editar_solicitud/',editar_solicitud),
    path('eliminar_producto/<id_producto>',eliminar_producto), 
    path('listar_datos',listar_datos),
    path('modificar_datos',modificar_datos),
    path('subir_oferta',subir_oferta),
    path('subir_oferta1/',subir_oferta_listado),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

