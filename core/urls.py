from django.urls import path
from .views import *

urlpatterns = [
<<<<<<< HEAD
    path('', name='home'),
    path('', name='registro'),
    path('', name='agente')
=======
    path('', home, name='home')
    path('',registro, name='registro')
    
>>>>>>> 05815bb2d7eabb55c6dda725994d81c32b895275
]