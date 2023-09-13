from django import forms
from .models import Order


class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
