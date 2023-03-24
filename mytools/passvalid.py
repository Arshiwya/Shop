symbols = ['!', '@', '#', '$', '&', '*']

password = 'arshiya90poma@'
# [0] >>>>>>> the validator
# [1] >>>>>>> error text


def pass_validator(password):
    if len(password) < 8:
        error = 'رمز عبور کوتاه می باشد . حداقل 8 کارکتر وارد کنید .'
        return False, error

    valid = False

    for c in password:

        for s in symbols:

            if c == s:
                valid = True
                break

        if valid == True :
            break

    if valid:
        return True, ''

    else:
        error = 'برای رمز عبور حداقل یکی از این کاراکتر ها الزامی است . [! / @ / # / $ / % / &]'
        return False, error


