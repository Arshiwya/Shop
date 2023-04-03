from .models import Category
from accounts.models import User


def category_finder(request):
    if request.user.is_authenticated:
        user = request.user
        len_card = len(user.card.all())
    else:
        len_card = 0
    return {
        'all_categories': Category.objects.all()[:3],
        'len_card': len_card,
    }
