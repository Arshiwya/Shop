from django.urls import path
from .views import (index, products, admins_list, add_admin, delete_admin, edit_admin, change_password_admin,
                    send_reset_pass_link, reset_pass_admin, add_product, delete_product )
from django.contrib.auth.views import PasswordChangeView

app_name = 'panel'

urlpatterns = [

    path('', index, name='index'),
    path('products/', products, name='products'),
    path('admins/add/', add_admin, name='add_admin'),
    path('products/add/', add_product, name='add_product'),
    # path('products/edit/<slug:slug>/', edit_product, name='edit_product'),
    path('admins/list/<str:filter>/', admins_list, name='admins'),
    path('admins/edit/<str:username>/', edit_admin, name='edit_admin'),
    path('admins/delete/<str:username>/', delete_admin, name='delete_admin'),
    path('products/delete/<slug:slug>/', delete_product, name='delete_product'),
    path('admins/reset_pass/<str:token>/', reset_pass_admin, name='reset_pass_admin'),
    path('admins/send_reset_pass_email/', send_reset_pass_link, name='send_reset_pass_email'),
    path('admins/change_pass/<str:username>/', change_password_admin, name='change_pass_admin'),

]
