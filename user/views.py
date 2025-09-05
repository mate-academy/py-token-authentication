from typing import Any
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ManageUserSerializer,
)

User = get_user_model()


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args: Any, **kwargs: Any) -> Response:
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ManageUserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ManageUserSerializer

    def get_object(self) -> User:
        return self.request.user
