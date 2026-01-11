from datetime import datetime

from django.db.models import F, Count
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from cinema.permissions import IsAdminOrIfAuthenticatedReadOnly
from rest_framework.permissions import IsAuthenticated

from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession, Order

from cinema.serializers import (
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer,
    MovieSerializer,
    MovieSessionSerializer,
    MovieSessionListSerializer,
    MovieDetailSerializer,
    MovieSessionDetailSerializer,
    MovieListSerializer,
    OrderSerializer,
    OrderListSerializer,
)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class CinemaHallViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class MovieViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Movie.objects.prefetch_related("genres", "actors")
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            queryset = queryset.filter(
                genres__id__in=self._params_to_ints(genres)
            )

        if actors:
            queryset = queryset.filter(
                actors__id__in=self._params_to_ints(actors)
            )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer


class MovieSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    queryset = (
        MovieSession.objects.all()
        .select_related("movie", "cinema_hall")
        .annotate(
            tickets_available=(
                F("cinema_hall__rows")
                * F("cinema_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )

    def get_queryset(self):
        date = self.request.query_params.get("date")
        movie_id = self.request.query_params.get("movie")

        queryset = self.queryset

        if date:
            queryset = queryset.filter(
                show_time__date=datetime.strptime(date, "%Y-%m-%d").date()
            )

        if movie_id:
            queryset = queryset.filter(movie_id=int(movie_id))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        return MovieSessionSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie",
        "tickets__movie_session__cinema_hall",
    )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
