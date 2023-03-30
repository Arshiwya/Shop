from django import forms
from products.models import Category


class ProductForm(forms.Form):
    STATUS_CHOICE = (('d', 'draft'), ('p', 'published'),)
    categories = Category.objects.all()


    my_tuple = []
    for category in categories:
        my_tuple.append((category, category))
    CATEGORIES = tuple(my_tuple)


    name = forms.CharField(label='name', required=True, max_length=60)
    description = forms.CharField(label='description', required=False)
    slug = forms.SlugField(required=False, label='slug')
    price = forms.IntegerField(required=False, label='price')
    status = forms.ChoiceField(choices=STATUS_CHOICE, required=False, label='status')
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORIES, required=False,
                                           label='categories')
    discount_amount = forms.IntegerField(required=False, label='discount_amount')
    image = forms.ImageField(required=False, label='image')


class CommentForm(forms.Form):
    full_name = forms.CharField(label='full_name', required=True, max_length=80)
    email = forms.EmailField(label='email', required=True)
    text = forms.CharField(required=True, label='text', max_length=500)
