import functools
from rest_framework import status
from .models import User
from rest_framework.response import Response


def auth_required(view_func):
    @functools.wraps(view_func)
    def _auth_required(request, *args, **kwargs):
        if not getattr(request, 'token', None) or request.token.is_valid():
            return view_func(request, *args, **kwargs)
        return Response('Error token', status=status.HTTP_401_UNAUTHORIZED)

    return _auth_required


def admin_required(view_func):
    @functools.wraps(view_func)
    def _admin_required(request, *args, **kwargs):
        if getattr(request.token.user, 'role', None) == User.ADMIN:
            return view_func(request, *args, **kwargs)
        return Response('Error role', status=status.HTTP_403_FORBIDDEN)

    return _admin_required
