from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Category, Product


def home(request):
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
