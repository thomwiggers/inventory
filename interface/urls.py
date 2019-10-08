from django.urls import path, re_path

from interface import views

app_name = 'interface'

urlpatterns = [
    path('', views.ScannerView.as_view(), name='index'),
    re_path(r'^add_brand_ean/prefix/(?P<ean>\d{7})/$',
            views.AddBrandEANView.as_view(),
            name='add_brand_ean'),
    path('autocomplete/brand_autocomplete/',
         views.BrandAutocompleteView.as_view(),
         name='brand-autocomplete'),
]
