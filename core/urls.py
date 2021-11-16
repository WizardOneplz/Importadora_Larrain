from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

<<<<<<< HEAD
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
=======
urlpatterns = [  
    path('', name='/'),
    path('', name='registro'),
    path('', name='agente'),
    path('', name='home'),
    path('', name='registro'),
    path('', name='agente')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> a2a872eb956f516414de0b87ea344e8230cf1807
