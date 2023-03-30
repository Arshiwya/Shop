from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import (
    check_password, make_password
)
from django.core.mail import send_mail
from django.conf import settings

from mytools.passvalid import pass_validator
from mytools.usernamevalid import username_validator
from mytools.passwordchanger import pass_changer
from .models import User
from .forms import SigninForm, EditForm, ChangePasswordForm
from .mydecorators import log_in_checker


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


@login_required(login_url='/accounts/', redirect_field_name='next')
@log_in_checker
def edit_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        form = EditForm(initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'image': user.image,
            'is_superuser': user.is_superuser,

        })
        context = {
            'form': form,
            'type': 'edit',
        }

        return render(request, 'accounts/sign-in.html', context=context)

    elif request.method == 'POST':
        if request.FILES:
            files = request.FILES
        else:
            files = None

        form = EditForm(request.POST, files=files)

        if form.is_valid():
            if user.username != request.POST['username']:
                # check if username check or no
                username_check = username_validator(request.POST['username'])
                if username_check[0]:  # check the username's length
                    if not User.objects.filter(
                            username=request.POST['username']).exists():  # check if the new username exists or not
                        user.username = request.POST['username']

                    else:  # when the new username has already exists
                        message = 'این نام کاربری قبلا استفاده شده است !!!'
                        context = {
                            'form': form,
                            'message': message,
                            'type': 'edit',

                        }
                        return render(request, 'accounts/sign-in.html', context=context)

                else:  # when the new username's length is short
                    message = username_check[1]
                    context = {
                        'form': form,
                        'message': message,
                        'type': 'edit',

                    }
                    return render(request, 'accounts/sign-in.html', context=context)

            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            if user.email != request.POST['email']:

                if not User.objects.filter(email=request.POST['email']).exists():

                    user.email = request.POST['email']
                else:

                    message = 'این ایمیل قبلا ثبت شده است !!!'
                    context = {
                        'form': form,
                        'message': message,
                        'type': 'edit',
                        'admin': user
                    }
                    return render(request, 'accounts/sign-in.html', context=context)
                    # =====================================================================

            if files:  # change the image if a file uploaded
                user.image = files['image']

                # =====================================================================

                # =====================================================================

            if 'image-clear' in request.POST:  # change the current image to default

                user.image = 'profiles/defult_prof.jpg'

                # =====================================================================

            user.save()
            return redirect('products:home')

        else:
            print(form.errors)
            print('c' * 200)


@login_required(login_url='/accounts/', redirect_field_name='next')
@log_in_checker
def change_pass_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        form = ChangePasswordForm()
        context = {
            'form': form,
            'user': user,
        }

        return render(request, 'accounts/change_pass_user.html', context=context)

    elif request.method == 'POST':

        correct_old_pass = user.password
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_pass = request.POST['old_password']
            new_password1 = request.POST['new_password1']
            new_password2 = request.POST['new_password2']

            if check_password(old_pass, correct_old_pass):
                pass_check = pass_changer(new_password1, new_password2)
                if pass_check[0]:
                    pass_check2 = pass_validator(new_password1)

                    if pass_check2[0]:

                        User.objects.filter(username=username).update(password=make_password(new_password1))
                        message = 'رمز عبور با موفقیت تغییر کرد .'
                        send_mail(

                            subject=' تغییر گذرواژه',

                            message=f'''
کاربر گرامی گذرواژه شما تغییر کرد .



                                        ''',

                            from_email=settings.EMAIL_HOST_USER,

                            recipient_list=[(User.objects.get(username=username)).email])

                        return redirect('products:home')

                    else:
                        message = pass_check2[1]
                        form = ChangePasswordForm()
                        context = {
                            'form': form,
                            'message': message,
                            'user': user,

                        }

                        return render(request, 'accounts/change_pass_user.html', context=context)

                else:
                    message = pass_check[1]
                    form = ChangePasswordForm()
                    context = {
                        'form': form,
                        'message': message,
                        'user': user,

                    }

                    return render(request, 'accounts/change_pass_user.html', context=context)

            else:
                message = 'رمز عبور قدیمی وارد شده صحیح نمی باشد !!!'
                form = ChangePasswordForm()
                context = {
                    'form': form,
                    'message': message,
                    'user': user,

                }

                return render(request, 'accounts/change_pass_user.html', context=context)

        else:
            message = 'اطلاعات ورودی نامعتبر می باشد !!!'
            form = ChangePasswordForm()
            context = {
                'form': form,
                'message': message,
                'user': user,
            }

            return render(request, 'accounts/change_pass_user.html', context=context)
