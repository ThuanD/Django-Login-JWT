from django.db import models
import jwt
from datetime import datetime, timedelta
from django.conf import settings
# Create your models here.


class User(models.Model):
    MEMBER = 0
    ADMIN = 1

    username = models.CharField(blank=False, null=False, max_length=255)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    role = models.IntegerField(default=0)

    class Meta:
        db_table = 'login'
        unique_together = (('username', 'password'),)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        exp = datetime.now() + timedelta(days=1)
        iat = datetime.now()
        payload = {
            'id': str(self.id),
            'role': str(self.role),
            'exp': exp,
            'iat': iat,
            'username': self.username,
            'password': self.password,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')