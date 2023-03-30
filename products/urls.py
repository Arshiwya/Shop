from django.urls import path, include
from .views import home, single_product, search_product, category_products, send_comment

app_name = 'products'

urlpatterns = [

    path('', home, name='home'),
    path('send_comment/', send_comment, name='send_comment'),
    path('product/<slug:slug>/', single_product, name='product'),
    path('product/search/<slug:text>/', search_product, name='search'),
    path('product/category/<slug:slug>/', category_products, name='category'),

]
