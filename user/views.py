from django.contrib.auth import get_user_model

from rest_framework.generics import (CreateAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.serializers import UserSerializer


User = get_user_model()


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class MeView(RetrieveAPIView, UpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
