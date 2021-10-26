from django.urls import path
from .views import *

urlpatterns = [
    path('', name='home'),
    path('', name='registro'),
    path('', name='agente')
]