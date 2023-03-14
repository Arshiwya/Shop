import random, string


def get_random(length):
    letters = string.ascii_lowercase
    letters += string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

