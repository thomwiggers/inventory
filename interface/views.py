from dal import autocomplete

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, CreateView
from django.db.models import Q

from interface import forms
from interface.models import (
    Brand, BrandEAN, Product, Packaging, GenericProduct)


class ScannedItemView(View):
    def get(self, request, ean):
        packaging = get_object_or_404(Packaging, label=ean)

        return render(request, 'interface/scanned_item.html', {
            'packaging': packaging,
            'product': packaging.product,
        })

    def post(self, request, ean):
        packaging = get_object_or_404(Packaging, label=ean)
        action = request.POST.get('action')
        if action not in ('add', 'subtract'):
            return HttpResponseBadRequest(f"bad action: {action!r}")
        product = packaging.product
        if action == 'add':
            product.count += packaging.count
        else:
            product.count -= packaging.count
        try:
            product.save()
        except ValidationError:
            messages.error(request, "We can't have negative counts!")

        return redirect(
            reverse('interface:scanned_item', kwargs={'ean': ean}))


class ScannerView(FormView):
    form_class = forms.ProductScannerForm
    template_name = 'interface/index.html'

    def form_valid(self, form):
        ean = form.cleaned_data['ean']

        try:
            Brand.by_ean(ean)
        except Brand.DoesNotExist:
            return redirect('interface:add_brand_ean', ean=ean)

        try:
            Product.by_ean(ean)
        except Product.DoesNotExist:
            return redirect('interface:select_product_for_packaging', ean=ean)

        return redirect('interface:scanned_item', ean=ean)


class AddBrandEANView(CreateView):
    model = BrandEAN
    form_class = forms.BrandEANAddForm

    def get_success_url(self):
        return reverse(
            'interface:select_product_for_packaging',
            kwargs={'ean': self.kwargs.get('ean')})

    def get_initial(self):
        initial = super().get_initial()
        if 'ean' in self.kwargs:
            initial['label'] = str(self.kwargs['ean'] // 10**6)
        return initial


class CreatePackagingView(CreateView):
    model = Packaging
    success_url = reverse_lazy('interface:index')
    fields = '__all__'

    def get_form(self):
        form = super().get_form()
        form.fields['label'].disabled = True
        form.fields['product'].disabled = True
        return form

    def get_context_data(self):
        context = super().get_context_data()
        context['product'] = get_object_or_404(
            Product, pk=self.kwargs['product'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['label'] = self.kwargs['ean']
        initial['product'] = self.kwargs['product']
        return initial


class SelectProductView(View):
    template_name = 'interface/select_product.html'
    success_target = ''

    def get(self, request, ean):
        brand = Brand.by_ean(ean)
        select_product_form = forms.SelectProductForm(brand=brand)
        product_form = forms.ProductForm(initial={'brand': brand})

        return render(request, self.template_name, {
            'select_product_form': select_product_form,
            'product_form': product_form,
        })

    def post(self, request, ean):
        brand = Brand.by_ean(ean)
        product_id = request.POST.get('product')
        if product_id:
            product = get_object_or_404(Product, brand=brand, pk=product_id)
        else:
            product_form = forms.ProductForm(request.POST)
            if not product_form.is_valid():
                return render(request, self.template_name, {
                    'select_product_form':
                        forms.SelectProductForm(brand=brand),
                    'product_form': product_form,
                })
            product = product_form.save()
        return redirect(
            reverse(self.success_target,
                    kwargs={
                        'product': product.pk,
                        'ean': ean,
                    }))


class BrandAutocompleteView(autocomplete.Select2QuerySetView):
    create_field = 'name'

    def get_queryset(self):
        qs = Brand.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ProductAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Product.objects.all().order_by('name')
        brand = self.forwarded.get('brand')
        if brand:
            qs = qs.filter(brand=brand)
        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) | Q(brand__name__icontains=self.q))
        return qs


class GenericProductAutocompleteView(autocomplete.Select2QuerySetView):
    create_field = 'name'

    def get_queryset(self):
        qs = GenericProduct.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
