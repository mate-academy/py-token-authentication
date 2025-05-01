from datetime import datetime

from django.db.models import F, Count
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers

from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession, Order
from cinema.permissions import IsAdminOrIfAuthenticatedReadOnly, IsOwnerOrAdmin

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


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.prefetch_related("genres", "actors")
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.select_related("movie", "cinema_hall")
    serializer_class = MovieSessionSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        return MovieSessionSerializer

    def get_queryset(self):
        date = self.request.query_params.get("date")
        movie_id = self.request.query_params.get("movie")

        queryset = self.queryset

        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
                queryset = queryset.filter(show_time__date=date)
            except ValueError:
                raise serializers.ValidationError(
                    {"date": "Invalid date format. Use YYYY-MM-DD"}
                )

        if movie_id:
            try:
                movie_id = int(movie_id)
                queryset = queryset.filter(movie_id=movie_id)
            except ValueError:
                raise serializers.ValidationError(
                    {"movie": "Movie ID must be an integer"}
                )

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie", "tickets__movie_session__cinema_hall"
    )
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]
    pagination_class = OrderPagination

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
