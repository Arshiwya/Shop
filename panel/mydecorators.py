## my custom decorator for test if user is superuser or want to see his page
from django.shortcuts import redirect


def check_user(func):
    def wrapper(request, username):
        if request.user.is_superuser or request.user.username == username:
            return func(request, username)
        else:
            return redirect('/accounts/denied/')

    return wrapper
