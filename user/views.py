from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class LoginUserView(ObtainAuthToken):

    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):

        return self.request.user
