from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from user.models import User
from user.serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [AllowAny()]


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
