from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from mytools.passvalid import pass_validator
from mytools.usernamevalid import username_validator
from .models import User
from .forms import SigninForm


# Create your views here.


def log_in(request):
    if 'next' in request.GET:
        next_page = request.GET['next']
    else:
        next_page = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)
            if next_page != '':
                return redirect(to=next_page)

            else:
                if user.is_superuser or user.is_staff:
                    return redirect(to='panel:index')
                else:
                    return redirect(to='products:home')


        else:
            error = 'نام کاربری یا رمز عبور اشتباه است . دوباره تلاش کنید!!!'
            context = {
                'error': error,
            }

            return render(request, 'accounts/login.html', context=context)

    else:
        return render(request, 'accounts/login.html')


def log_out(request):
    logout(request)

    return redirect('products:home')


def sign_in(request):
    message = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if request.FILES:
            files = request.FILES
        else:
            files = None

        form = SigninForm(request.POST, files=files)
        if form.is_valid():
            if not User.objects.filter(username=username).exists():

                username_check = username_validator(username)
                password_check = pass_validator(password)

                if username_check[0]:
                    if password_check[0]:
                        first_name = request.POST['first_name']
                        last_name = request.POST['last_name']
                        email = request.POST['email']
                        if request.FILES:
                            image = request.FILES['image']

                        else:
                            image = 'profiles/defult_prof.jpg'

                        User.objects.create_user(username=username, password=password, email=email,
                                                 first_name=first_name,
                                                 last_name=last_name, image=image)
                        user = User.objects.get(username=username)
                        login(request, user)

                        return redirect('products:home')


                    else:

                        message = password_check[1]


                else:
                    message = username_check[1]

                form = SigninForm()
                context = {
                    'message': message,
                    'form': form,
                }

                return render(request, 'accounts/sign-in.html', context=context)



            else:
                message = 'این نام کاربری قبلا استفاده شده است !!!'
                form = SigninForm()
                context = {
                    'message': message,
                    'form': form,
                }

                return render(request, 'accounts/sign-in.html', context=context)


    else:
        form = SigninForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/sign-in.html', context=context)


def denied(request):
    return render(request, 'accounts/access-denied.html')
