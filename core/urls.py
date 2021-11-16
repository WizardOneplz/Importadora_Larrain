from django.urls import path
from .views import *

urlpatterns = [

    
    path('', name='home'),
    path('', name='registro'),
    path('', name='agente'),
    path('', name='login'),
    path('', home, name='home'),
    path('', registro, name='registro'),
    path('', login , name='login'),
    path('', name='home'),
    path('', name='registro'),
    path('', name='agente'),
    path('', name='login')
]