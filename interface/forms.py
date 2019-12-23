from dal import autocomplete, forward
from django import forms

from interface import models
from interface.fields import EANFormField


class ProductScannerForm(forms.Form):
    ean = EANFormField()


class PackagingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Packaging
        exclude = ['product']


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Product
        exclude = ['count']
        widgets = {
            'brand': autocomplete.ModelSelect2(
                url='interface:brand-autocomplete',
            ),
        }


class SelectProductForm(forms.Form):
    def __init__(self, *args, brand, **kwargs):
        super().__init__(*args, **kwargs)
        if brand is not None:
            self.fields['product'].queryset = brand.product_set.all()
            self.fields['product'].widget.forward = [
                forward.Const(brand.pk, 'brand')]

    product = forms.ModelChoiceField(
        queryset=models.Product.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='interface:product-autocomplete',
        ),
    )
