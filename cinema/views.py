from datetime import datetime

from django.db.models import F, Count
from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession, Order
from cinema.permissions import (
    AuthenticationMixin,
    IsAdminOrIfAuthenticatedReadOnly
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


class GenreViewSet(
    AuthenticationMixin,
    ListModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Genre endpoint.
    AuthenticationMixin applies TokenAuthentication and
    IsAdminOrIfAuthenticatedReadOnly permission.
    Admins can create, authenticated users can read/write
    according to custom permission logic.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(
    AuthenticationMixin,
    ListModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Actor endpoint.
    AuthenticationMixin ensures token auth
    and custom permission are applied globally.
    """
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(
    AuthenticationMixin,
    ListModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    CinemaHall endpoint.
    Same permission logic as Genre/Actor.
    """
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(
    AuthenticationMixin,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    Movie endpoint with filtering support.
    AuthenticationMixin provides token auth + IsAdminOrIfAuthenticatedReadOnly.
    """
    queryset = Movie.objects.prefetch_related("genres", "actors")
    serializer_class = MovieSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer

        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer


class MovieSessionViewSet(
    AuthenticationMixin,
    ModelViewSet,
):
    """
    MovieSession endpoint.
    Permission explicitly set to IsAdminOrIfAuthenticatedReadOnly
    to override AuthenticationMixin if needed.
    Admins can manage all sessions, authenticated users can read safely.
    """
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        date = self.request.query_params.get("date")
        movie_id_str = self.request.query_params.get("movie")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if movie_id_str:
            queryset = queryset.filter(movie_id=int(movie_id_str))

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
    AuthenticationMixin,
    ListModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Order endpoint.
    Explicitly sets IsAuthenticated because orders
    are private and only visible to the owner.
    TokenAuthentication is inherited from AuthenticationMixin.
    """
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie",
        "tickets__movie_session__cinema_hall"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    # only authenticated users can access
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
