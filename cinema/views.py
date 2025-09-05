from datetime import datetime

from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

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


class BaseReadCreateViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class GenreViewSet(BaseReadCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(BaseReadCreateViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(BaseReadCreateViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Movie.objects.prefetch_related("genres", "actors")
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def _parse_ids(self, param: str) -> list[int]:
        try:
            return [int(x) for x in param.split(",") if x.strip().isdigit()]
        except Exception:
            return []

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        title = params.get("title")
        genres = self._parse_ids(params.get("genres", ""))
        actors = self._parse_ids(params.get("actors", ""))

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genres:
            queryset = queryset.filter(genres__id__in=genres)
        if actors:
            queryset = queryset.filter(actors__id__in=actors)

        return queryset.distinct()

    def get_serializer_class(self):
        return {
            "list": MovieListSerializer,
            "retrieve": MovieDetailSerializer,
        }.get(self.action, MovieSerializer)


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.select_related(
        "movie", "cinema_hall"
    ).annotate(
        tickets_available=F("cinema_hall__rows")
        * F("cinema_hall__seats_in_row")
        - Count("tickets")
    )
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        date_str = params.get("date")
        movie_id_str = params.get("movie")

        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(show_time__date=date)
            except ValueError:
                pass

        if movie_id_str and movie_id_str.isdigit():
            queryset = queryset.filter(movie_id=int(movie_id_str))

        return queryset

    def get_serializer_class(self):
        return {
            "list": MovieSessionListSerializer,
            "retrieve": MovieSessionDetailSerializer,
        }.get(self.action, MovieSessionSerializer)


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie", "tickets__movie_session__cinema_hall"
    )
    pagination_class = OrderPagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        return (
            OrderListSerializer if self.action == "list" else OrderSerializer
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
