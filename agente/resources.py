from import_export import resources
from core.models import Oferta

class OfertaResource(resources.ModelResource):
    class meta:
        model = Oferta
