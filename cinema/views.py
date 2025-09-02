from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrIfAuthenticatedReadOnly
from .models import (
    Genre, CinemaHall, Actor, Movie, MovieSession, Order
)
from .serializers import (
    GenreSerializer, CinemaHallSerializer, ActorSerializer,
    MovieListSerializer, MovieDetailSerializer,
    MovieSessionListSerializer, MovieSessionDetailSerializer,
    MovieSessionWriteSerializer,
    OrderListCreateSerializer, OrderCreateSerializer,
)


class OrderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ---- Genres: list + create ----
class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


# ---- Halls: list + create ----
class CinemaHallViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


# ---- Actors: list + create ----
class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


# ---- Movies: list + retrieve + create ----
class MovieViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Movie.objects.all().prefetch_related(
        "genres", "actors"
    )
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieListSerializer


# ---- Sessions: list + retrieve + CRUD ----
class MovieSessionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = MovieSession.objects.select_related(
        "movie", "cinema_hall"
    )
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        if self.action == "list":
            return MovieSessionListSerializer
        return MovieSessionWriteSerializer


# ---- Orders: list + create (для автентифікованих) ----
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = OrderPagination

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related(
                "tickets",
                "tickets__movie_session__movie",
                "tickets__movie_session__cinema_hall",
            )
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderListCreateSerializer

    def perform_create(self, serializer):
        serializer.save()
