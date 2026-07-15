from datetime import datetime

from django.db.models import F, Count, QuerySet

from rest_framework import generics
from rest_framework.serializers import BaseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from cinema.models import (
    Genre,
    Actor,
    CinemaHall,
    Movie,
    MovieSession,
    Order
)

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


class GenreApiView(
    generics.ListCreateAPIView
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorApiView(
    generics.ListCreateAPIView
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallApiView(
    generics.ListCreateAPIView
):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieDetailApiView(generics.RetrieveAPIView):
    queryset = Movie.objects.prefetch_related(
        "genres",
        "actors"
    )
    serializer_class = MovieDetailSerializer


class MovieApiView(
    generics.ListCreateAPIView
):
    queryset = Movie.objects.prefetch_related(
        "genres",
        "actors"
    )
    serializer_class = MovieSerializer

    @staticmethod
    def _params_to_ints(qs: str) -> list[int]:
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self) -> QuerySet[Movie]:
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        queryset = super().get_queryset()

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors_ids)

        return queryset.distinct()

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return MovieListSerializer

        return MovieSerializer


class MovieSessionDetailApiView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = (
        MovieSession.objects.all()
        .select_related("movie", "cinema_hall")
        .annotate(
            tickets_available=F("cinema_hall__rows")
            * F("cinema_hall__seats_in_row")
            - Count("tickets")
        )
    )
    serializer_class = MovieSessionSerializer

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return MovieSessionDetailSerializer

        return MovieSessionSerializer


class MovieSessionApiView(
    generics.ListCreateAPIView
):
    queryset = (
        MovieSession.objects.all()
        .select_related("movie", "cinema_hall")
        .annotate(
            tickets_available=F("cinema_hall__rows")
            * F("cinema_hall__seats_in_row")
            - Count("tickets")
        )
    )
    serializer_class = MovieSessionSerializer

    def get_queryset(self) -> QuerySet[MovieSession]:
        date = self.request.query_params.get("date")
        movie_id_str = self.request.query_params.get("movie")

        queryset = super().get_queryset()

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if movie_id_str:
            queryset = queryset.filter(movie_id=int(movie_id_str))

        return queryset

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return MovieSessionListSerializer

        return MovieSessionSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderApiView(
    generics.ListCreateAPIView
):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie",
        "tickets__movie_session__cinema_hall"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Order]:
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(user=self.request.user)
