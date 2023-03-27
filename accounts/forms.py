from django import forms


class SigninForm(forms.Form):
    username = forms.CharField(label='username', required=True, max_length=60)
    password = forms.CharField(label='password', required=True, max_length=60)
    first_name = forms.CharField(label='first_name', required=False, max_length=60)
    last_name = forms.CharField(label='last_name', required=False, max_length=60)
    email = forms.EmailField(label='email', required=True)
    image = forms.ImageField(label='image', required=False, allow_empty_file=True)
