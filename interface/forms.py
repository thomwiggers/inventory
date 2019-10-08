from django import forms

from interface.models import Brand, BrandEAN
from interface.fields import EANFormField


class ProductScannerForm(forms.Form):
    ean = EANFormField()


class BrandEANAddForm(forms.Form):
    ean_prefix = forms.CharField(max_length=7, help_text="Brand EAN prefix")

    #: Specify if you want to create a new brand
    new_brand = forms.CharField(
        max_length=255,
        help_text="New brand name",
        required=False,
    )

    #: Refer to an existing brand instead of creating a new one
    existing_brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        help_text="OR existing brand",
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        new_brand = cleaned_data.get('new_brand')
        if (new_brand and cleaned_data.get('existing_brand')):
            err = forms.ValidationError(
                "Either specify a new brand or an existing one, not both",
                code="duplicate"
            )
            self.add_error('new_brand', err)
            self.add_error('existing_brand', err)
        if new_brand:
            if Brand.objects.filter(name=new_brand).exists():
                self.add_error(
                    'new_brand',
                    forms.ValidationError(
                        'Brand "%(brand_name)s" already exists.',
                        code='duplicate',
                        params={'brand_name': new_brand})
                )

        if BrandEAN.objects.filter(label=cleaned_data['ean_prefix']).exists():
            obj = Brand.by_ean(cleaned_data['ean_prefix'])
            self.add_error(
                'ean_prefix',
                forms.ValidationError(
                    'EAN prefix "%(ean_prefix)s" already registered to brand '
                    '"%(brand)s".',
                    code='duplicate',
                    params={
                        'ean_prefix': cleaned_data['ean_prefix'],
                        'brand': obj.name,
                    })
            )
        return cleaned_data

    def save(self):
        brand = self.cleaned_data.get('existing_brand')
        if brand is None:
            brand = Brand.objects.create(name=self.cleaned_data['new_brand'])
        BrandEAN.objects.create(
            label=self.cleaned_data['ean_prefix'],
            brand=brand,
        )
