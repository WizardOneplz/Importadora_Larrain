from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from cart.views import *  #esto se debe hacer cada vez que se quiera importar una views de las otras APPS
from . import views

app_name = 'cart'
urlpatterns = [
    path('', cart, name='order_create'),
    path('create/', views.order_create, name='order_create'),
    path('agregar/<int:id_producto>/', agregar_carrito, name="Add"),
    path('eliminar/<int:id_producto>', eliminar_carrito, name="Del" ),
    path('restar/<int:id_producto>', restar_carrito, name="Sub" ),
]