from .models import Category


def category_finder(request):
    return {
        'all_categories':Category.objects.all()[:3],
    }