from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from cinema.models import (
    Genre,
    Actor,
    CinemaHall,
    Movie,
    MovieSession,
    Order,
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
from cinema.permissions import IsAdminOrIfAuthenticatedReadOnly


class OrderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all().order_by("id")
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Actor.objects.all().order_by("id")
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CinemaHallViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CinemaHall.objects.all().order_by("id")
    serializer_class = CinemaHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class MovieViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Movie.objects.all().order_by("id")
    serializer_class = MovieSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genre_ids = [int(str_id) for str_id in genres.split(",")]
            queryset = queryset.filter(genres__id__in=genre_ids)

        if actors:
            actor_ids = [int(str_id) for str_id in actors.split(",")]
            queryset = queryset.filter(actors__id__in=actor_ids)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("genres", "actors")

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer

        if self.action == "retrieve":
            return MovieDetailSerializer

        return MovieSerializer


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all().order_by("id")
    serializer_class = MovieSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        movie = self.request.query_params.get("movie")
        date = self.request.query_params.get("date")

        if movie:
            queryset = queryset.filter(movie_id=int(movie))

        if date:
            queryset = queryset.filter(show_time__date=date)

        if self.action == "list":
            capacity = (
                F("cinema_hall__rows") * F("cinema_hall__seats_in_row")
            )
            queryset = (
                queryset
                .select_related("movie", "cinema_hall")
                .annotate(
                    tickets_count=Count("tickets"),
                    tickets_available=capacity - F("tickets_count")
                )
            )

        if self.action == "retrieve":
            queryset = (
                queryset
                .select_related("movie", "cinema_hall")
                .prefetch_related("tickets")
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer

        if self.action == "retrieve":
            return MovieSessionDetailSerializer

        return MovieSessionSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__movie_session__movie",
                "tickets__movie_session__cinema_hall"
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
