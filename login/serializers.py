from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
