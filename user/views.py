from rest_framework import generics
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = [AllowAny]


class ManagerUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
