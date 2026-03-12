from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'note', 'amount', 'created_at']
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }