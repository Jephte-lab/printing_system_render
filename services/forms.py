# services/forms.py
from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = Service
        fields = ['name', 'base_price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service name'
            }),
            'base_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Base price'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }
