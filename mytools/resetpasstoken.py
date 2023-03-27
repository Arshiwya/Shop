import random, string


def reset_token():
    letters = string.ascii_lowercase
    letters += string.digits
    result_str = ''.join(random.choice(letters) for i in range(20))
    return result_str

