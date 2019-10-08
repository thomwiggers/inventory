from dal import autocomplete

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView, CreateView

from interface.forms import ProductScannerForm, BrandEANAddForm
from interface.models import Brand, BrandEAN, Product


class ScannerView(FormView):
    form_class = ProductScannerForm
    template_name = 'interface/index.html'

    def form_valid(self, form):
        ean = form.cleaned_data['ean']

        try:
            brand = Brand.by_ean(ean)
        except Brand.DoesNotExist:
            return redirect('interface:add_brand_ean', ean=ean[:7])

        try:
            product = Product.by_ean(ean)
        except Product.DoesNotExist:
            return HttpResponse(f"Add product form with {brand} for {ean}")

        return HttpResponse(f"done: {product}")


class AddBrandEANView(CreateView):
    model = BrandEAN
    form_class = BrandEANAddForm
    success_url = reverse_lazy('interface:index')

    def get_initial(self):
        initial = super().get_initial()
        if 'ean' in self.kwargs:
            initial['label'] = self.kwargs['ean']
        return initial


class BrandAutocompleteView(autocomplete.Select2QuerySetView):
    create_field = 'name'

    def get_queryset(self):
        qs = Brand.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
