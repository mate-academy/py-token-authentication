from django.urls import path, include
from rest_framework import routers

from cinema.views import (
    GenreView,
    ActorView,
    CinemaHallView,
    MovieListView,
    MovieDetailView,
    MovieSessionViewSet,
    OrderView,
)

router = routers.DefaultRouter()
router.register("movie_sessions", MovieSessionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("genres/", GenreView.as_view(), name="genre-list"),
    path("actors/", ActorView.as_view(), name="actor-list"),
    path("cinema_halls/", CinemaHallView.as_view(), name="cinemahall-list"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("orders/", OrderView.as_view(), name="order-list")
]

app_name = "cinema"
