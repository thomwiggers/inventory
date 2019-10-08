from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from interface.forms import ProductScannerForm, BrandEANAddForm
from interface.models import Brand, Product


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


class AddBrandEANView(FormView):
    form_class = BrandEANAddForm
    success_url = reverse_lazy('interface:index')
    template_name = 'interface/brand_form.html'

    def get_initial(self):
        initial = super().get_initial()
        if 'ean' in self.kwargs:
            initial['ean_prefix'] = self.kwargs['ean']
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
