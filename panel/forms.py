from django import forms
from django.forms import ModelForm
from accounts.models import User


# class EditAdminForm(ModelForm):
#     username = forms.CharField(label='username', required=True, max_length=60)
#     # password = forms.CharField(label='password', required=True, max_length=60)
#     first_name = forms.CharField(label='first_name', required=False, max_length=60)
#     last_name = forms.CharField(label='last_name', required=False, max_length=60)
#     email = forms.EmailField(label='email', required=False)
#     image = forms.ImageField(label='image', required=False, allow_empty_file=True)
#     is_superuser = forms.BooleanField(label='super user', required=False, initial=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'image', 'is_superuser']


class AddAdminForm(forms.Form):
    username = forms.CharField(label='username', required=True, max_length=60)
    password = forms.CharField(label='password', required=True, max_length=60)
    first_name = forms.CharField(label='first_name', required=False, max_length=60)
    last_name = forms.CharField(label='last_name', required=False, max_length=60)
    email = forms.EmailField(label='email', required=True)
    image = forms.ImageField(label='image', required=False, allow_empty_file=True)
    is_superuser = forms.BooleanField(label='super user', required=False, initial=False)


class EditAdminForm(forms.Form):
    username = forms.CharField(label='username', required=True, max_length=60)
    first_name = forms.CharField(label='first_name', required=False, max_length=60)
    last_name = forms.CharField(label='last_name', required=False, max_length=60)
    email = forms.EmailField(label='email', required=True)
    image = forms.ImageField(label='image', required=False, allow_empty_file=True)
    is_superuser = forms.BooleanField(label='super user', required=False, initial=False)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='password', required=True, max_length=60)
    new_password1 = forms.CharField(label='password', required=True, max_length=60)
    new_password2 = forms.CharField(label='password', required=True, max_length=60)


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='password', required=True, max_length=60)
    new_password2 = forms.CharField(label='password', required=True, max_length=60)


class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField(required=True, label='email')
