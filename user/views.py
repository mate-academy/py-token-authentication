from rest_framework import generics, settings
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserTokenCreateView(ObtainAuthToken):
    renderer_classes = settings.api_settings.DEFAULT_RENDERER_CLASSES
