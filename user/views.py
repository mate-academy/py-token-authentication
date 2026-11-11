from rest_framework import generics, permissions
from user.serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(ObtainAuthToken):
    pass


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
