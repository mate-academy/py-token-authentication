from datetime import datetime
from django.db.models import F, Count
from django.utils.timezone import make_aware
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

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
    MovieDetailSerializer,
    OrderSerializer,
    MovieSessionSerializer,
    MovieSessionListSerializer,
    MovieSessionDetailSerializer,
)
from cinema.permissions import IsAdminOrIfAuthenticatedReadOnly


class GenreViewSet(GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ActorViewSet(GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CinemaHallViewSet(GenericViewSet, mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class MovieViewSet(GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Movie.objects.prefetch_related("genres", "actors")
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer


class MovieSessionViewSet(GenericViewSet, mixins.ListModelMixin,
                          mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = (
        MovieSession.objects.all()
        .select_related("movie", "cinema_hall")
        .annotate(
            tickets_available=(
                F("cinema_hall__rows") *
                F("cinema_hall__seats_in_row") -
                Count("tickets")
            )
        )
    )
    serializer_class = MovieSessionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        qs = self.queryset
        date = self.request.query_params.get("date")
        if date:
            dt = datetime.strptime(date, "%Y-%m-%d")
            qs = qs.filter(show_time__date=make_aware(dt))
        movie_id = self.request.query_params.get("movie")
        if movie_id:
            qs = qs.filter(movie_id=int(movie_id))
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        return MovieSessionSerializer


class OrderPagination(PageNumberPagination):
    max_page_size = 100


class OrderViewSet(GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie",
        "tickets__movie_session__cinema_hall",
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": len(serializer.data),
            "results": serializer.data,
        })
