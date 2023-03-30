
def username_validator(username):

    length = len(username)

    if length < 5:
        error = 'نام کاربری باید حداقل 5 کاراکتر باشد .'
        return False, error

    else:
        return True , 'is_valid'



