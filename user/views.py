from rest_framework import generics, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.serializers import api_settings
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = (AllowAny, )


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

