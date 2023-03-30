from django.contrib import admin
from django.urls import path, include
from .views import log_in, log_out, sign_in, denied, edit_user , change_pass_user

app_name = 'accounts'

urlpatterns = [

    path('', log_in, name='login'),
    path('denied/', denied, name='denied'),
    path('logout/', log_out, name='logout'),
    path('signin/', sign_in, name='signin'),
    path('edit/<str:username>/', edit_user, name='edit_user'),
    path('change_pass/<str:username>/', change_pass_user, name='change_pass_user'),

]
