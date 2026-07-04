from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.serializers import CustomUserSerializer


class CreateUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class MeApiView(RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
