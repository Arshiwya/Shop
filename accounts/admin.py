from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# For Hashin password in admin panel


class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets[0][1]['fields'] += ('image',)
    UserAdmin.fieldsets[1][1]['fields'] += ('balance',)
    UserAdmin.fieldsets[3][1]['fields'] += ('special_til',)

    list_display = ['username', 'email', 'balance', 'is_superuser']
    ordering = ['-date_joined']


admin.site.register(User, CustomUserAdmin)
