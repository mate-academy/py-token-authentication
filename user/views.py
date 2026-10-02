"""Public registration/login and private profile endpoints."""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import api_settings

from user.models import User
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Register a regular user."""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CreateTokenView(ObtainAuthToken):
    """Validate credentials and return a reusable authentication token."""

    permission_classes = (AllowAny,)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Read or update only the authenticated user's profile."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
