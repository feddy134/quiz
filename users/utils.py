
import random
import string
from django.conf import settings

DEFAULT_RANDOM_STRING_LENGTH = 8


def get_random_alphanumeric_string(string_length=DEFAULT_RANDOM_STRING_LENGTH,
                                   lowercase=True,
                                   uppercase=True,
                                   digits=True):
    """
    Create random alphanumeric string of given length and characterset
    """
    scope = ''
    if lowercase:
        scope += string.ascii_lowercase
    if uppercase:
        scope += string.ascii_uppercase
    if digits:
        scope += string.digits
    return ''.join(random.choice(scope) for _ in range(string_length))


def get_username(user):
    """
    Create random username for given user based on their name
    """
    if user.last_name:
        username = f'{user.first_name}_{user.last_name}_{get_random_alphanumeric_string()}'
    elif user.first_name:
        username = f'{user.first_name}_{get_random_alphanumeric_string()}'
    else:
        username = f'user_{get_random_alphanumeric_string()}'
    username = username.replace(' ', '_')
    from .models import User
    existing_user = User.objects.filter(username=username).first()
    if existing_user:
        return get_username(user)
    return username


def name_to_first_name_and_last_name(name):
    """
    Splits a single string of name into first and last name
    """
    name_list = name.split()
    first_name = name_list[0]
    last_name = ''
    if len(name) > 1:
        last_name = ' '.join(name_list[1:])
    return (first_name, last_name)
