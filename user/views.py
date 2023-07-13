from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateTokenView(views.ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
