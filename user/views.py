from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.settings import api_settings

from user.serializers import (UserSerializer,
                              UserUpdateSerializer, UserCreateSerializer
                              )

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UserUpdateSerializer
