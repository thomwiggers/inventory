from django.urls import path

from interface import views

app_name = 'interface'

urlpatterns = [
    path('', views.ScannerView.as_view(), name='index'),
    path('select_product_for_packaging/ean/<str:ean>/',
         views.SelectProductView.as_view(
             success_target='interface:add_packaging'),
         name='select_product_for_packaging'),
    path('packaging/add/product/<int:product>/ean/<str:ean>/',
         views.CreatePackagingView.as_view(),
         name='add_packaging'),
    path('packaging/ean/<str:ean>/',
         views.PackagingView.as_view(),
         name='packaging'),

    # Autocomplete forms
    path('autocomplete/brand_autocomplete',
         views.BrandAutocompleteView.as_view(),
         name='brand-autocomplete'),
    path('autocomplete/product_autocomplete',
         views.ProductAutocompleteView.as_view(),
         name='product-autocomplete'),
]
