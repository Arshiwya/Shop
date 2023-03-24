
def username_validator(username):

    length = len(username)

    if length < 6:
        error = 'نام کاربری باید حداقل 6 کاراکتر باشد .'
        return False, error

    else:
        return True , 'is_valid'



