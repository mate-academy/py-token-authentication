from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()


class ManageUserView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
