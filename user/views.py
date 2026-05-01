from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """POST api/user/register/"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CreateTokenView(ObtainAuthToken):
    """POST api/user/login/"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """GET/PUT/PATCH api/user/me/"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Возвращает текущего аутентифицированного пользователя"""
        return self.request.user
