from datetime import datetime
from .models import User


class AbstractToken(object):
    def __init__(self):
        self._errors = []

    @property
    def id(self):
        return None

    @property
    def expire_at(self):
        return None

    @property
    def created_at(self):
        return None

    @property
    def user(self):
        return None

    def is_valid(self):
        return False


class UnauthorizedToken(AbstractToken):
    def __init__(self, *errors):
        super(UnauthorizedToken, self).__init__()
        self._errors = errors


class Token(AbstractToken):
    def __init__(self, id, expire_at, created_at, jwt):
        super(Token, self).__init__()
        self._id = id
        self._created_at = created_at if isinstance(created_at, datetime)\
                else datetime.fromtimestamp(created_at)
        self._expire_at = expire_at if isinstance(expire_at, datetime)\
                else datetime.fromtimestamp(expire_at)
        self._jwt = jwt

    @property
    def id(self):
        return self._id

    @property
    def expire_at(self):
        return self._expire_at

    @property
    def created_at(self):
        return self._created_at

    @property
    def jwt(self):
        return self._jwt

    @property
    def user(self):
        if hasattr(self, '_user'):
            return self._user
        try:
            self._user = self._get_user()
            return self._user
        except User.DoesNotExist:
            return None

    def _get_user(self):
        try:
            return User.objects.get(id=self._id)
        except User.DoesNotExist:
            return None

    def is_valid(self):
        if self.user is None:
            return False
        return True
