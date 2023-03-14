from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# For Hashin password in admin panel


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'balance', 'is_superuser']
    ordering = ['-date_joined']


admin.site.register(User, CustomUserAdmin)
