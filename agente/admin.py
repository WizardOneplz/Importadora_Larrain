from django.contrib import admin
from core.models import Oferta
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here. 

class OfertaAdmin(ImportExportModelAdmin):
    list_display = ('id_oferta','rut_proveedor','nombre_proveedor','apellido_proveedor','email','oferta','fecha','empleado_rut')