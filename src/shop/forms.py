from django import forms
from django.core.exceptions import ValidationError

from shop.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address"]
        widgets = {"address": forms.Textarea(attrs={"class": "form-control"})}

    def clean_address(self):
        address = self.cleaned_data["address"]

        if len(address) < 5:
            raise ValidationError("Address must consist of at least 5 characters")

        return address
