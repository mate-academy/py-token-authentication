from django.urls import path

from cinema.views import (
    GenreApiView,
    ActorApiView,
    CinemaHallApiView,
    MovieApiView,
    MovieDetailApiView,
    MovieSessionApiView,
    MovieSessionDetailApiView,
    OrderApiView,
)


urlpatterns = [
    path("actors/", ActorApiView.as_view(), name="actor-list"),
    path("orders/", OrderApiView.as_view(), name="order-list"),
    path("genres/", GenreApiView.as_view(), name="genre-list"),
    path(
        "cinema_halls/",
        CinemaHallApiView.as_view(),
        name="cinemahall-list"
    ),
    path("movies/", MovieApiView.as_view(), name="movie-list"),
    path(
        "movies/<int:pk>/",
        MovieDetailApiView.as_view(),
        name="movie-detail"
    ),
    path(
        "movie_sessions/",
        MovieSessionApiView.as_view(),
        name="moviesession-list"
    ),
    path(
        "movie_sessions/<int:pk>/",
        MovieSessionDetailApiView.as_view(),
        name="moviesession-detail"
    ),
]

app_name = "cinema"
