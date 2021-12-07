from django import forms
from django.forms import widgets
from core.models import OrdenCompra

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['nombre_comprador',
                  'apellido_comprador', 'tipo_pago_id_tipo_pago', 'tipo_orden_id_tipo_orden', 'cuenta_cliente_email']
        widgets = {}

class CartAddProductForm(forms.Form):
    cantidad = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
