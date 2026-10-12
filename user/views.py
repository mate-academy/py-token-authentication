from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from user.serializers import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class LoginWithTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagePersonalInfo(RetrieveUpdateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user
