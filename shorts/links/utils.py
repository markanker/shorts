from random import choices, randint
from string import ascii_letters, digits
from exceptions import ValidationError
from links.models import Link
import re

RANDOM_LINK_CHARS = ascii_letters + digits + '-_'
SHORT_REGULAR_EXPR = r'[A-Za-z\d\-_]{1,15}'


def validate_short(short):
    if not re.findall(SHORT_REGULAR_EXPR, short):
        raise ValidationError("the name for a short link you gave is not proper. "
                              "It must only contain '-', '_', a-z, A-Z and digits "
                              "and be less than 16 characters")
    return short


def get_valid_data_from_post_request(request):
    data = request.data.copy()
    if not (request.user.is_authenticated and data.get('short_link')):
        data['short_link'] = ''.join(choices(RANDOM_LINK_CHARS, k=randint(5, 15)))
    else:
        data['short_link'] = validate_short(data['short_link'])
    if request.user.is_authenticated:
        data['user'] = request.user.id
    elif request.session.session_key:
        data['session_key'] = request.session.session_key
    else:
        raise ValidationError('you must either have set the session_key or be authorized')
    return data


def switch_session_to_user(user, session_key):
    if session_key:
        link_not_auth = Link.objects.filter(session_key=session_key)
        link_not_auth.user = user
        link_not_auth.session_key = None
        link_not_auth.save()
