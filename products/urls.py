from django.urls import path, include
from .views import home, single_product, search_product, category_products, send_comment, add_to_card, remove_from_card, card_list

app_name = 'products'

urlpatterns = [

    path('', home, name='home'),
    path('send_comment/', send_comment, name='send_comment'),
    path('product/<slug:slug>/', single_product, name='product'),
    path('product/card/card_list/', card_list, name='card_list'),
    path('product/add_to_card/<slug:slug>/', add_to_card, name='add_to_card'),
    path('product/remove_from_card/<slug:slug>/', remove_from_card, name='remove_from_card'),
    path('product/search/<slug:text>/', search_product, name='search'),
    path('product/category/<slug:slug>/', category_products, name='category'),

]
