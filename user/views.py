from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
        }, status=status.HTTP_200_OK)


class MeView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # return the currently authenticated user
        return self.request.user
