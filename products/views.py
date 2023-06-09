from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Product
from django.db.models import Q
from .forms import CommentForm
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User


def home(request):
    if request.GET.get('search'):
        text = request.GET.get('search')
        search_result = Product.objects.filter(
            Q(name__contains=text) | Q(slug__contains=text) | Q(description__contains=text))
        return search_product(request, search_result, text)

        # return redirect(to=f'/product/search/{request.GET.get("search")}/')

    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'products/index.html', context=context)


def single_product(request, slug):
    if request.GET.get('search'):
        text = request.GET.get('search')
        search_result = Product.objects.filter(
            Q(name__contains=text) | Q(slug__contains=text) | Q(description__contains=text))
        return search_product(request, search_result, text)

    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product,

    }

    return render(request, 'products/single-product.html', context=context)


def search_product(request, search_result, text):
    context = {
        'search_result': search_result,
        'text': text,
    }

    return render(request, 'products/search-result.html', context=context)


def category_products(request, slug):
    if request.GET.get('search'):
        text = request.GET.get('search')
        search_result = Product.objects.filter(
            Q(name__contains=text) | Q(slug__contains=text) | Q(description__contains=text))
        return search_product(request, search_result, text)
    category = get_object_or_404(Category, slug=slug)

    context = {
        'category': category,
    }

    return render(request, 'products/category-products.html', context=context)


def send_comment(request):
    if request.GET.get('search'):
        text = request.GET.get('search')
        search_result = Product.objects.filter(
            Q(name__contains=text) | Q(slug__contains=text) | Q(description__contains=text))
        return search_product(request, search_result, text)
    if request.method == 'GET':
        form = CommentForm()
        context = {
            'form': form,
        }

        return render(request, 'comment.html', context=context)

    else:
        form = CommentForm(request.POST)
        if form.is_valid():

            text = form.cleaned_data.get('text')
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            send_mail(

                subject=f"دیدگاه {full_name}",

                message=f'''
{text}        

ادرس ایمیل : {email}    



                                        ''',

                from_email=settings.EMAIL_HOST_USER,

                recipient_list=['arshiyasohrabi81@gmail.com'])
            form = CommentForm()
            context = {
                'form': form,
            }

            return redirect('products:home')


        else:
            print('hi')

@login_required(login_url='/accounts/', redirect_field_name='next')
def add_to_card(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    user.card.add(product)
    return single_product(request, slug)

@login_required(login_url='/accounts/', redirect_field_name='next')
def remove_from_card(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    user.card.remove(product)
    return card_list(request)

@login_required(login_url='/accounts/?next=/panel/admins/', redirect_field_name='next')
def card_list(request):
    if request.GET.get('search'):
        text = request.GET.get('search')
        search_result = Product.objects.filter(
            Q(name__contains=text) | Q(slug__contains=text) | Q(description__contains=text))
        return search_product(request, search_result, text)
    user = request.user
    products = user.card.all()
    context = {
        'products': products,
    }

    return render(request, 'products/card_list.html', context=context)
