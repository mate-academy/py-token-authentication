from rest_framework import generics
from rest_framework.authtoken import views
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserLoginAPIView(views.ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
