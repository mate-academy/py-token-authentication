from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, UserUpdateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserUpdateSerializer
    http_method_names = ["get", "put", "patch"]

    def get_object(self):
        return self.request.user
