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
from home.views import *  #esto se debe hacer cada vez que se quiera importar una views de las otras APPS
from registro.views import *
from administrador.views import *
from bodeguero.views import *
from cliente.views import *
from agente.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',home),
    path('registro',registro,),
    path('agregar_empleado',agregar_empleado),
    path('mantenedor_productos',mantenedor_productos),
    path('listar_datos',listar_datos),
    path('modificar_datos',modificar_datos),
    path('subir_oferta',subir_oferta),
]
