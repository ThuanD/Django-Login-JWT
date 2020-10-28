from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import User
from .serializers import UserSerializer, ProfileSerializer, UserModelSerializer
from django.utils.decorators import method_decorator
from .decorators import auth_required
# Create your views here.


class LoginView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        request_body = UserSerializer(data=request.data)
        if not request_body.is_valid():
            return Response(request_body.errors, status=status.HTTP_400_BAD_REQUEST)
        print('body', request_body)
        data = request_body.validated_data
        print('data', data)
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return Response({'message': 'Account does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'token': user.token, 'role': user.role}, status=status.HTTP_200_OK)


class ProfileView(GenericAPIView):

    serializer_class = ProfileSerializer

    @method_decorator(auth_required)
    def get(self, request):
        me = request.token.user
        serializer = UserModelSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(auth_required)
    def put(self, request):
        me = request.token.user

        request_body = ProfileSerializer(data=request.data)
        if not request_body.is_valid():
            return Response({'message': 'Cannot found account.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request_body.validated_data
        me.full_name = data.get('full_name', me.full_name)
        me.save()

        serializer = UserModelSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)