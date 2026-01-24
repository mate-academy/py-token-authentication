# user/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserMeSerializer

User = get_user_model()


# POST api/user/register/
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer


# POST api/user/login/
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            # Linha quebrada para não exceder 79 caracteres
            return Response(
                {"detail": "Usuário ou senha inválidos."}, status=401
            )


# GET/PUT/PATCH api/user/me/
class UserMeView(generics.RetrieveUpdateAPIView):
    # Permitir acesso apenas para usuários autenticados
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserMeSerializer

    def get_object(self):
        # Retorna o usuário atualmente autenticado
        return self.request.user

    def get_queryset(self):
        # Garantir que o queryset seja apenas o usuário atual (para RetrieveUpdateAPIView funcionar com get_object)
        # Linha quebrada para não exceder 79 caracteres
        return User.objects.filter(pk=self.request.user.pk)
