from django.contrib import admin
from django.urls import path, include
from .views import log_in, log_out , sign_in

app_name = 'accounts'

urlpatterns = [

    path('', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('signin/', sign_in, name='signin'),

]
