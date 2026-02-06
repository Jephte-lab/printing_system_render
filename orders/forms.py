# orders/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from clients.models import Client
from services.models import Service


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'name', 'status']

        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=('service', 'quantity', 'unit_price'),
    extra=0,                # 🔑 IMPORTANT: do NOT force empty forms
    can_delete=True,
    widgets={
        'service': forms.Select(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    }
)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['service', 'quantity', 'unit_price']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)
