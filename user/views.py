from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """POST api/user/register/"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """POST api/user/login/ — retorna token para credenciais válidas."""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH api/user/me/
    Requer token. Atualiza o próprio usuário (inclui troca de senha).
    """
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
