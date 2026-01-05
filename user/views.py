from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserMeSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
