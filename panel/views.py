from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AddAdminForm, EditAdminForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordEmailForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import (
    check_password, make_password
)
from django.core.mail import send_mail
from django.conf import settings

from products.models import Product
from accounts.models import User

from mytools.passvalid import pass_validator
from mytools.usernamevalid import username_validator
from mytools.passwordchanger import pass_changer
from mytools.resetpasstoken import reset_token


# ======================test=========================

def staff_checker(user):
    if user.is_staff:
        return True
    else:
        return False


def superuser_checker(user):
    if user.is_superuser:
        return True
    else:
        return False


# ======================test=========================

@login_required(login_url='/accounts/?next=/panel', redirect_field_name='next')
@user_passes_test(staff_checker, login_url='/accounts/denied/')
def index(request):
    # send_mail(
    #
    #     subject='Add an eye-catching subject',
    #
    #     message='سلام علیگم شما وارد شدید',
    #
    #     from_email=settings.EMAIL_HOST_USER,
    #
    #     recipient_list=['arshiyasohrabi81@gmail.com'])

    return render(request, 'panel/index.html')


@login_required(login_url='/accounts/?next=/panel', redirect_field_name='next')
@user_passes_test(staff_checker, login_url='/accounts/denied/')
def products(request):
    context = {
        'products': Product.objects.all(),
    }

    return render(request, 'panel/products.html', context=context)


@login_required(login_url='/accounts/?next=/panel/admins/', redirect_field_name='next')
@user_passes_test(superuser_checker, login_url='/accounts/denied/')
def admins_list(request):
    if 'message' in request.session:
        message = request.session['message']
        del request.session['message']
    else:
        message = None
    admins = User.objects.filter(is_staff=True)

    context = {
        'admins': admins,
        'message': message,

    }

    return render(request, 'panel/admins_list.html', context=context)


@login_required(login_url='/accounts/?next=/panel/admins/add', redirect_field_name='next')
@user_passes_test(superuser_checker, login_url='/accounts/denied/')
def add_admin(request):
    if request.method == 'GET':

        form = AddAdminForm()
        context = {
            'form': form,
            'type': 'add'
        }

        return render(request, 'panel/add_edit_admin.html', context=context)



    elif request.method == 'POST':

        if request.FILES:
            files = request.FILES
        else:
            files = None

        form = AddAdminForm(request.POST, files=files)

        if form.is_valid():
            if not User.objects.filter(username=request.POST['username']).exists():
                username = request.POST['username']
                password = request.POST['password']

                username_check = username_validator(username)
                password_check = pass_validator(password)

                if username_check[0]:
                    if password_check[0]:
                        first_name = request.POST['first_name']
                        last_name = request.POST['last_name']

                        if not User.objects.filter(email=request.POST['email']).exists():
                            email = request.POST['email']

                        else:
                            message = f'این ایمیل قبلا ثبت شده است ==>    {request.POST["email"]}  '
                            form = AddAdminForm()
                            context = {
                                'form': form,
                                'message': message,
                                'type': 'add'

                            }
                            return render(request, 'panel/add_edit_admin.html', context=context)

                        if request.FILES:
                            image = request.FILES['image']

                        else:
                            image = 'profiles/defult_prof.jpg'
                        if 'is_superuser' in request.POST:
                            is_superuser = True
                        else:
                            is_superuser = False

                        User.objects.create_user(username=username, password=password, email=email,
                                                 first_name=first_name,
                                                 last_name=last_name, image=image, is_staff=True,
                                                 is_superuser=is_superuser)

                        return redirect('panel:admins')


                    else:

                        message = password_check[1]


                else:
                    message = username_check[1]

                form = AddAdminForm()
                context = {
                    'message': message,
                    'form': form,
                    'type': 'add'
                }

                return render(request, 'panel/add_edit_admin.html', context=context)


            else:
                message = 'این نام کاربری قبلا استفاده شده است !!!'
                form = AddAdminForm()
                context = {
                    'message': message,
                    'form': form,
                    'type': 'add'
                }

                return render(request, 'panel/add_edit_admin.html', context=context)


@login_required(login_url='/accounts/?next=/panel/admins/add', redirect_field_name='next')
@user_passes_test(superuser_checker, login_url='/accounts/denied/')
def delete_admin(request, username):
    if len(User.objects.filter(is_staff=True)) != 1:
        user = get_object_or_404(User, username=username)
        user.delete()

        return redirect('panel:admins')

    else:
        request.session['message'] = 'شما نمی توانید آخرین مدیر را حذف کنید !!!'

        return redirect('panel:admins')


@login_required(login_url='/accounts/?next=/panel/admins/', redirect_field_name='next')
@user_passes_test(superuser_checker, login_url='/accounts/denied/')
def edit_admin(request, username):
    admin = get_object_or_404(User, username=username)
    if request.method == 'GET':

        form = EditAdminForm(initial={
            'username': admin.username,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
            'email': admin.email,
            'image': admin.image,
            'is_superuser': admin.is_superuser,

        })
        context = {
            'form': form,
            'type': 'edit',
            'admin': admin
        }
        return render(request, 'panel/add_edit_admin.html', context=context)

    elif request.method == 'POST':
        if request.FILES:
            files = request.FILES
        else:
            files = None

        form = EditAdminForm(request.POST, files=files)

        if form.is_valid():
            if admin.username != request.POST['username']:
                 # check if username check or no
                username_check = username_validator(request.POST['username'])
                if username_check[0]:  # check the username's length
                    if not User.objects.filter(
                            username=request.POST['username']).exists():  # check if the new username exists or not
                        admin.username = request.POST['username']

                    else:  # when the new username has already exists
                        message = 'این نام کاربری قبلا استفاده شده است !!!'
                        context = {
                            'form': form,
                            'message': message,
                            'type': 'edit',
                            'admin': admin
                        }
                        return render(request, 'panel/add_edit_admin.html', context=context)

                else:  # when the new username's length is short
                    message = username_check[1]
                    context = {
                        'form': form,
                        'message': message,
                        'type': 'edit',
                        'admin': admin
                    }
                    return render(request, 'panel/add_edit_admin.html', context=context)

            admin.last_name = request.POST['last_name']
            admin.first_name = request.POST['first_name']
            if admin.email != request.POST['email']:

                if not User.objects.filter(email=request.POST['email']).exists():

                    admin.email = request.POST['email']
                else:

                    message = 'این ایمیل قبلا ثبت شده است !!!'
                    context = {
                        'form': form,
                        'message': message,
                        'type': 'edit',
                        'admin': admin
                    }
                    return render(request, 'panel/add_edit_admin.html', context=context)
                    # =====================================================================

            if files:  # change the image if a file uploaded
                admin.image = files['image']

                    # =====================================================================

            if 'is_superuser' in request.POST:  # change the superuser status
                admin.is_superuser = True
            else:
                admin.is_superuser = False

                    # =====================================================================

            if 'image-clear' in request.POST:  # change the current image to default

                admin.image = 'profiles/defult_prof.jpg'

                    # =====================================================================

            admin.save()
            return redirect('panel:admins')






        else:  # when an image is uploaded and also the clear checkbox is turned on. form is invalid
            message = 'لطفا یا یک عکس انتخاب کنید یا تیک پاک کردن عکس را بزنید . نه هر دو !!!'
            form = EditAdminForm(initial={
                'username': admin.username,
                'first_name': admin.first_name,
                'last_name': admin.last_name,
                'email': admin.email,
                'image': admin.image,
                'is_superuser': admin.is_superuser,

            })
            context = {
                'form': form,
                'type': 'edit',
                'message': message,
                'admin': admin,
            }
            return render(request, 'panel/add_edit_admin.html', context=context)


@login_required(login_url='/accounts/?next=/panel/admins/', redirect_field_name='next')
@user_passes_test(superuser_checker, login_url='/accounts/denied/')
def change_password_admin(request, username):
    admin = get_object_or_404(User, username=username)
    correct_old_pass = admin.password

    if request.method == 'GET':
        form = ChangePasswordForm()
        context = {
            'form': form,

        }

        return render(request, 'panel/change_password.html', context=context)

    elif request.method == 'POST':
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
کاربر گرامی گذرواژه شما از طریق پنل ادمین تغییر کرد .



                            ''',

                            from_email=settings.EMAIL_HOST_USER,

                            recipient_list=[(User.objects.get(username=username)).email])

                        return redirect('panel:admins')

                    else:
                        message = pass_check2[1]
                        form = ChangePasswordForm()
                        context = {
                            'form': form,
                            'message': message

                        }

                        return render(request, 'panel/change_password.html', context=context)

                else:
                    message = pass_check[1]
                    form = ChangePasswordForm()
                    context = {
                        'form': form,
                        'message': message,

                    }

                    return render(request, 'panel/change_password.html', context=context)

            else:
                message = 'رمز عبور قدیمی وارد شده صحیح نمی باشد !!!'
                form = ChangePasswordForm()
                context = {
                    'form': form,
                    'message': message,

                }

                return render(request, 'panel/change_password.html', context=context)

        else:
            message = 'اطلاعات ورودی نامعتبر می باشد !!!'
            form = ChangePasswordForm()
            context = {
                'form': form,
                'message': message,

            }

            return render(request, 'panel/change_password.html', context=context)


def reset_pass_admin(request, token):
    if request.method == 'GET':

        admin = get_object_or_404(User, reset_pass_token=token)
        form = ResetPasswordForm()
        context = {
            'form': form,
            'admin': admin,
        }
        return render(request, 'panel/reset_pass_admin.html', context=context)

    elif request.method == 'POST':
        admin = get_object_or_404(User, reset_pass_token=token)
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        pass_check = pass_changer(new_password1, new_password2)

        if pass_check[0]:
            pass_check2 = pass_validator(new_password1)
            if pass_check2[0]:
                User.objects.filter(reset_pass_token=token).update(password=make_password(new_password1))
                User.objects.filter(reset_pass_token=token).update(reset_pass_token=reset_token())
                messsage = 'رمز عبور شما با موفقیت تغییر کرد .'
                context = {
                    'message': messsage,
                }
                return render(request, 'panel/send_email_success.html', context=context)

            else:
                message = pass_check2[1]
                form = ResetPasswordForm()
                context = {
                    'form': form,
                    'message': message,
                    'admin': admin,
                }
                return render(request, 'panel/reset_pass_admin.html', context=context)

        message = pass_check[1]
        form = ResetPasswordForm()
        context = {
            'form': form,
            'message': message,
            'admin': admin,
        }
        return render(request, 'panel/reset_pass_admin.html', context=context)


def send_reset_pass_link(request):
    if request.method == 'GET':
        form = ResetPasswordEmailForm()
        context = {
            'form': form,
        }

        return render(request, 'panel/send_reset_email.html', context=context)

    if request.method == 'POST':
        form = ResetPasswordEmailForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                token = (User.objects.get(email=email)).reset_pass_token
                send_mail(

                    subject='درخواست تغییر گذرواژه',

                    message=f'''
                    برای تغییر گذرواژه خود از لینک زیر استفاده کنید 
                    http://127.0.0.1:8000/panel/admins/reset_pass/{token}/
                    
                    
                    
                    ''',

                    from_email=settings.EMAIL_HOST_USER,

                    recipient_list=[email])

                return render(request, 'panel/send_email_success.html')

            else:
                message = 'ادرس ایمیل ثبت نشده است !'
                form = ResetPasswordEmailForm()
                context = {
                    'form': form,
                    'message': message,
                }

                return render(request, 'panel/send_reset_email.html', context=context)


        else:
            message = 'ادرس ایمیل معتبر نمی باشد !'
            form = ResetPasswordEmailForm()
            context = {
                'form': form,
                'message': message,
            }

            return render(request, 'panel/send_reset_email.html', context=context)
