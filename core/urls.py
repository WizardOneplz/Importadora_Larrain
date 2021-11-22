from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [  
    path('', name='/'),
    path('', name='registro'),
    path('', name='agente'),
    path('', name='home'),
    path('', name='registro'),
    path('', name='agente')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)