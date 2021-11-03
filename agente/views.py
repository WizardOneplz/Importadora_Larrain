from django.shortcuts import render, redirect
from django.db import connection
from tablib import Dataset 
from core.models import Oferta
from .resources import OfertaResource
from django.contrib import messages
from django.http import HttpResponse
import cx_Oracle

# Create your views here.

def listado_ofertas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_OFERTAS",[out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def subir_oferta(request):
    data = {
        'ofertas':listado_ofertas(),
    }
    return render(request,'subir_oferta.html',data)

def subir_oferta_listado(request):
       #template = loader.get_template('export/importar.html')
    if request.method == 'POST':
        #template = loader.get_template('export/importar.html')  if request.method == 'POST':  
        oferta_resource = OfertaResource()
        dataset = Dataset()
        #print(dataset)  
        nuevas_ofertas = request.FILES['myfile']

        if not nuevas_ofertas.name.endswith('xlsx'):
            messages.info(request,'Formato Archivo Incorrecto')
            return render(request, 'subir_oferta.html',{})
        imported_data = dataset.load(nuevas_ofertas.read(),format='xlsx')
        messages.info(request,'Archivo Añadido Correctamente')
        for data in imported_data:
            value = Oferta(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                )
            value.save()
    return redirect('/subir_oferta')
    
    
 




