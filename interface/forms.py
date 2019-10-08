from dal import autocomplete

from django import forms

from interface.models import BrandEAN
from interface.fields import EANFormField


class ProductScannerForm(forms.Form):
    ean = EANFormField()


class BrandEANAddForm(forms.ModelForm):
    class Meta:
        model = BrandEAN
        fields = ['label', 'brand']
        widgets = {
            'brand': autocomplete.ModelSelect2(
                url='interface:brand-autocomplete'),
        }
