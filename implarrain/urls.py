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
    path('', home, name='home'),
    path('store', store),
    path('cart/', include('cart.urls', namespace='cart')),
    path('producto/<int:pk>/', producto, name='producto'),
    path('oferta', oferta),
    path('categoria/<int:id_categoria>', categoria, name='categoria'),
    path('marca/<int:id_marca>', marca, name='marca'),
    path('search', search),

    #REGISTRO
    path('registro',registro,),
    path('seguimiento', seguimiento),
    path('mostrar_info/', mostrarinfo),
    #REGISTRO
    path('registro',registro),
    path('logemp/agregar_empleado',mantenedor_admin),
    path('login', login), 
    path('cerrarsesion',cerrarsesion),
    path('perfil/<cliente_rut>',modificar_cliente),
    path('editar_perfil/',perfil),
    path('logemp/',logemp),
    path('logemp/logout',logout),
    path('<empleado_rut>/peremple',modificar_perfil),
    path('edt_emple/',peremple),
    #ELIMINAR
    path('logemp/eliminar_empleado/<rut>',eliminar_empleado),
    path('eliminar_estanteria/<id_estanteria>',eliminar_estanteria),
    path('eliminar_pasillo/<id_pasillo>',eliminar_pasillo),
    path('eliminar_bodega/<id_bodega>',eliminar_bodega),
    path('logemp/eliminar_marca/<id_marca>',eliminar_marca),
    path('logemp/eliminar_categoria/<id_categoria>',eliminar_categoria),
    #MANTENEDORES
    path('logemp/mantenedor_bodega',mantenedor_bodega),
    path('logemp/mantenedor_pasillo',mantenedor_pasillo),
    path('logemp/mantenedor_estanteria',mantenedor_estanteria),
    path('logemp/mantenedor_marca',mantenedor_marca),
    path('logemp/mantenedor_categorias',mantenedor_categorias),
    path('logemp/mantenedor_productos',mantenedor_productos),
    #MODIFICAR
    path('logemp/modificar_marca/<id_marca>',modificar_marca),
    path('editar_marca/',editar_marca),
    path('logemp/modificar_categoria/<id_categoria>',modificar_categoria),
    path('editar_categoria/',editar_categoria),
    path('logemp/modificar_bodega/<id_bodega>',modificar_bodega),
    path('editar_bodega/',editar_bodega),
    path('logemp/modificar_empleado/<rut>',modificar_empleado),
    path('editar_empleado/',editar_empleado),
    path('logemp/modificar_orden/<id_orden>',modificar_orden),
    path('editar_orden/',editar_orden),
    path('logemp/modificar_producto/<id_producto>',modificar_producto),
    path('logemp/modificar_solicitud/<id_solicitud>',modificar_solicitud),
    path('editar_producto/',editar_producto),
    path('editar_solicitud/',editar_solicitud),
    path('logemp/eliminar_producto/<id_producto>',eliminar_producto), 
    path('modificar_datos',modificar_datos),
    path('logemp/subir_oferta',subir_oferta),
    path('subir_oferta1/',subir_oferta_listado),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

