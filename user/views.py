from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer, UserRegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/user/register/"""
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(ObtainAuthToken):
    """POST /api/user/login/ → {"token": "..."}"""
    permission_classes = [permissions.AllowAny]
    # Нічого не перевизначаємо: базовий клас сам валідить
    # і повертає {"token": "<...>"} або 400 на невалідні дані.


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/user/me/"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
