from django.urls import path

from interface import views

app_name = 'interface'

urlpatterns = [
    path('', views.ScannerView.as_view()),
    path('add_brand/', views.AddBrandView.as_view()),
]
