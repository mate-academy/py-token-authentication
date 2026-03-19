from datetime import datetime

from django.db.models import F, Count
from rest_framework.renderers import (
    BrowsableAPIRenderer, JSONRenderer
)
from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import DEFAULTS

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


class GenreViewSet(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(ListCreateAPIView):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ViewSet):
    queryset = Movie.objects.all().prefetch_related(
        "genres", "actors"
    )

    @staticmethod
    def query_params_to_int_list(query_params: str) -> list:
        return [int(i) for i in query_params.split(",")]

    def list(self, request):
        title = request.query_params.get("title", None)
        genres = request.query_params.get("genres", None)
        actors = request.query_params.get("actors", None)

        if title:
            self.queryset = self.queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self.query_params_to_int_list(genres)
            self.queryset = self.queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self.query_params_to_int_list(actors)
            self.queryset = self.queryset.filter(actors__id__in=actors_ids)

        serializer = MovieListSerializer(self.queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieSessionViewSet(viewsets.ModelViewSet):
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
    serializer_class = MovieSessionSerializer

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


class OrderCreateListViewSet(viewsets.ViewSet):
    # The style to use for queryset pagination.
    pagination_class = OrderPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.prefetch_related(
            "tickets__movie_session__movie",
            "tickets__movie_session__cinema_hall"
        ).filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrderListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset, self.request, view=self
        )

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
