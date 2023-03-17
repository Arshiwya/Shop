from django.urls import path, include
from .views import home, single_product , search_product

app_name = 'products'

urlpatterns = [

    path('', home, name='home'),
    path('product/<slug:slug>/', single_product, name='product'),
    path('product/search/<slug:text>/', search_product, name='search'),

]
