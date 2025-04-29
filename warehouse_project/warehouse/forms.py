from django import forms
from .models import Product, Shipment, ShipmentItem, Supply, SupplyItem
from django.forms import inlineformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity', 'image']

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['supplier']

class SupplyItemForm(forms.ModelForm):
    class Meta:
        model = SupplyItem
        fields = ['product', 'quantity']

SupplyItemFormSet = inlineformset_factory(
    Supply,
    SupplyItem,
    form=SupplyItemForm,
    extra=1,
    can_delete=True
)

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['client', 'client_address', 'client_phone', 'client_email', 'payment_status', 'delivery_date', 'shipping_method']

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['client', 'client_address', 'client_phone', 'client_email', 'payment_status', 'delivery_date', 'shipping_method']

ShipmentItemFormSet = inlineformset_factory(
    Shipment,
    ShipmentItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True
)

