def pass_changer(new_pass1, new_pass2):
    if new_pass1 != new_pass2:
        return False, 'رمز عبور های جدید وارد شده یکسان نمی باشند !!!'

    else:
        return True, 'یکسان'
