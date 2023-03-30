from django.shortcuts import render, redirect, get_object_or_404


def log_in_checker(func):
    def wrapper(request, username):
        if request.user.is_superuser:
            return func(request, username)

        else:
            if request.user.username != username:
                return redirect('/accounts/denied/')

            else:
                return func(request, username)

    return wrapper
