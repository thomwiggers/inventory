from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView, CreateView

from interface.forms import ProductScannerForm
from interface.models import Brand, Product


class ScannerView(FormView):
    form_class = ProductScannerForm
    template_name = 'interface/index.html'

    def form_valid(self, form):
        ean = form.cleaned_data['ean']

        try:
            brand = Brand.by_ean(ean)
        except Brand.DoesNotExist:
            return redirect('add_brand')

        try:
            product = Product.by_ean(ean)
        except Product.DoesNotExist:
            return HttpResponse(f"Add product form with {brand} for {ean}")

        return HttpResponse(f"done: {product}")


class AddBrandView(CreateView):
    model = Brand
    success_url = reverse_lazy('index')
    fields = ['name']
