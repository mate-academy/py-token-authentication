from typing import Type
from django.utils.dateparse import parse_date
from django.db.models import F, Count, Prefetch, QuerySet
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.pagination import PageNumberPagination

from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession, Order
from cinema.permissions import IsAdminOrIfAuthenticatedReadOnly
from cinema.serializers import (
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer,
    MovieSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSessionSerializer,
    MovieSessionListSerializer,
    MovieSessionDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    pagination_class = None

    def get_queryset(self) -> QuerySet[Genre]:
        queryset = self.queryset
        if self.action == "list":
            return queryset.only("id", "name")
        return queryset


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    pagination_class = None

    def get_queryset(self) -> QuerySet[Actor]:
        queryset = self.queryset
        if self.action == "list":
            return queryset.only("id", "first_name", "last_name")
        return queryset


class CinemaHallViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    pagination_class = None

    def get_queryset(self) -> QuerySet[CinemaHall]:
        queryset = self.queryset
        if self.action == "list":
            return queryset.only("id", "name", "rows", "seats_in_row")
        return queryset


class MovieViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    pagination_class = None

    @staticmethod
    def _params_to_ints(value: str) -> list[int]:
        """Convert '1,2,3' -> [1,2,3]"""
        return [int(x) for x in value.split(",") if x.strip().isdigit()]

    def get_queryset(self) -> QuerySet[Movie]:
        title_param = self.request.query_params.get("title")
        genres_param = self.request.query_params.get("genres")
        actors_param = self.request.query_params.get("actors")

        queryset: QuerySet[Movie] = self.queryset

        if title_param:
            queryset = queryset.filter(title__icontains=title_param)

        if genres_param:
            genre_ids = self._params_to_ints(genres_param)
            if genre_ids:
                queryset = queryset.filter(genres__id__in=genre_ids)

        if actors_param:
            actor_ids = self._params_to_ints(actors_param)
            if actor_ids:
                queryset = queryset.filter(actors__id__in=actor_ids)

        return queryset.distinct()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        MovieSession.objects.select_related("movie", "cinema_hall")
        .annotate(
            tickets_available=F(
                "cinema_hall__rows") * F(
                "cinema_hall__seats_in_row"
            ) - Count(
                "tickets"
            )
        )
    )
    serializer_class = MovieSessionSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    pagination_class = None

    def get_queryset(self) -> QuerySet[MovieSession]:
        date_param = self.request.query_params.get("date")
        movie_param = self.request.query_params.get("movie")

        queryset: QuerySet[MovieSession] = self.queryset

        if date_param:
            parsed_date = parse_date(str(date_param).strip())
            if parsed_date:
                queryset = queryset.filter(show_time__date=parsed_date)

        if movie_param:
            try:
                movie_id = int(str(movie_param).strip())
                queryset = queryset.filter(movie_id=movie_id)
            except (TypeError, ValueError):
                pass

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("tickets")

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
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
    viewsets.GenericViewSet
):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie", "tickets__movie_session__cinema_hall"
    ).order_by("id")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer: OrderSerializer) -> None:
        serializer.save(user=self.request.user)
