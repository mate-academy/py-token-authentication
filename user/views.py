from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import api_settings

from user.serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginUserView(ObtainAuthToken):
    """Login a user and return a token."""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the authenticated user."""
        return self.request.user


class UserListView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
