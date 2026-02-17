from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.AllowAny]


class UserLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
