from django import forms
from .models import Billing_Address

class Billing_Form(forms.ModelForm):
    class Meta:
        model = Billing_Address
        fields = ['address','zipcode','city','country']
