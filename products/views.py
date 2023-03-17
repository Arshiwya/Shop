from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Q


def home(request):
    if request.GET.get('search'):
        return redirect(to=f'/product/search/{request.GET.get("search")}/')

    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'products/index.html', context=context)

    # categories = Category.objects.all()
    # news_p = Product.objects.published()[:3]
    # best_sellers = Product.objects.all().order_by('-price')[:3]
    # discounters = Product.objects.discounters()[:3]
    # print(discounters)
    # context = {
    #
    #     'categories': categories,
    #     'products': news_p,
    #     'best_sellers': best_sellers,
    #     'discounts':discounters,
    # }


def single_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()[:4]
    context = {
        'product': product,
        'categories': categories,

    }

    return render(request, 'products/single-product.html', context=context)


def search_product(request, text):
    print(text)
    pr = ''
    products = Product.objects.filter(Q(name__contains=text) | Q(slug__contains=text))
    for p in products:
        pr += p.name

    return HttpResponse(pr)
