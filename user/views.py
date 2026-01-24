# user/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model  # ADICIONAR ESTA IMPORTAÇÃO
from .serializers import UserRegisterSerializer, UserMeSerializer

User = get_user_model()  # DEFINIR User AQUI, como feito nos serializers


# POST api/user/register/
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # Q000: Mudar para aspas duplas
    serializer_class = UserRegisterSerializer


# POST api/user/login/
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)  # Q000: Mudar para aspas duplas

    def post(self, request):
        username = request.data.get("username")  # Q000: Mudar para aspas duplas
        password = request.data.get("password")  # Q000: Mudar para aspas duplas
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})  # Q000: Mudar para aspas duplas
        else:
            return Response({"detail": "Usuário ou senha inválidos."}, status=401)  # Q000: Mudar para aspas duplas


# GET/PUT/PATCH api/user/me/
class UserMeView(generics.RetrieveUpdateAPIView):
    # Permitir acesso apenas para usuários autenticados
    permission_classes = (permissions.IsAuthenticated,)  # Q000: Mudar para aspas duplas
    serializer_class = UserMeSerializer

    def get_object(self):
        # Retorna o usuário atualmente autenticado
        return self.request.user

    def get_queryset(self):
        # Garantir que o queryset seja apenas o usuário atual (para RetrieveUpdateAPIView funcionar com get_object)
        return User.objects.filter(pk=self.request.user.pk)  # Q000: Mudar para aspas duplas
