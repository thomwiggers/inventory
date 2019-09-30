from django import forms

from interface.fields import EANFormField


class ProductScannerForm(forms.Form):
    ean = EANFormField()
