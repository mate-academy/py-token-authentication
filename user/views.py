from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import get_user_model
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserLoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
