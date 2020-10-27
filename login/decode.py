import jwt
from django.conf import settings
from rest_framework import exceptions
from .token import Token


def decode_token(token, algorithm='HS256'):
    try:
        raw_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[algorithm],
        )
    except jwt.exceptions.ExpiredSignatureError as e:
        raise exceptions.AuthenticationFailed(e.__str__())
    except Exception as e:
        raise exceptions.AuthenticationFailed(e.__str__())
    return Token(
        raw_token['id'],
        raw_token['exp'],
        raw_token['iat'],
        token
    )