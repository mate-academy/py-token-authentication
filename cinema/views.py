from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import (
    Genre,
    CinemaHall,
    Actor,
    Movie,
    MovieSession,
    Order,
)
from .serializers import (
    GenreSerializer,
    CinemaHallSerializer,
    ActorSerializer,
    MovieSerializer,
    MovieSessionSerializer,
    OrderSerializer,
)
from .permissions import IsAdminOrIfAuthenticatedReadOnly

User = get_user_model()


# --------------------------- USER ENDPOINTS ------------------------------

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []


class LoginAPIView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class UserMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


# ------------------------- CINEMA ENDPOINTS -----------------------------


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CinemaHallViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ActorViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class MovieViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    # todas as ações são permitidas:
    # list, retrieve, create, update, partial_update, destroy


# ----------------------- ORDER (ESPECIAL) -------------------------------

class OrderViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    - Apenas listar e criar
    - POST permitido para usuários autenticados (override da permissão)
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)  # <-- só aqui POST é permitido

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
