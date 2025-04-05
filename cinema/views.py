from datetime import datetime

from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination

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
from user.permissions import (
    IsAdminOrIfAuthenticatedReadOnly,
    IsOrderOwnerOrAdmin
)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class CinemaHallViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class MovieViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Movie.objects.prefetch_related("genres", "actors")
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        qs = self.queryset
        params = self.request.query_params

        if title := params.get("title"):
            qs = qs.filter(title__icontains=title)

        if genres := params.get("genres"):
            qs = qs.filter(genres__id__in=self._params_to_ints(genres))

        if actors := params.get("actors"):
            qs = qs.filter(actors__id__in=self._params_to_ints(actors))

        return qs.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        MovieSession.objects
        .select_related("movie", "cinema_hall")
        .annotate(
            tickets_available=F("cinema_hall__rows")
            * F("cinema_hall__seats_in_row")
            - Count("tickets")
        )
    )
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        qs = self.queryset
        params = self.request.query_params

        if date := params.get("date"):
            date = datetime.strptime(date, "%Y-%m-%d").date()
            qs = qs.filter(show_time__date=date)

        if movie_id := params.get("movie"):
            qs = qs.filter(movie_id=int(movie_id))

        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        return MovieSessionSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie",
        "tickets__movie_session__cinema_hall"
    )
    permission_classes = [IsOrderOwnerOrAdmin]
    pagination_class = OrderPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return OrderListSerializer if self.action == "list" else OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
