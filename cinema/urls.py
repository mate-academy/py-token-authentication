# cinema/urls.py
from django.urls import path
from .views import (
    AdminActorApiView, PrivateActorApiView,
    AdminCinemaHallApiView, PrivateCinemaHallApiView,
    AdminGenreApiView, PrivateGenreApiView,
    AdminMovieApiView, PrivateMovieApiView,
    PrivateMovieSessionApiView,
    PrivateOrderApiView,
)

app_name = "cinema"

urlpatterns = [
    # actors
    path("actors/", PrivateActorApiView.as_view()),
    path("actors/admin/", AdminActorApiView.as_view()),

    # cinema halls
    path("cinema-halls/", PrivateCinemaHallApiView.as_view()),
    path("cinema-halls/admin/", AdminCinemaHallApiView.as_view()),

    # genres
    path("genres/", PrivateGenreApiView.as_view()),
    path("genres/admin/", AdminGenreApiView.as_view()),

    # movies
    path("movies/", PrivateMovieApiView.as_view()),
    path("movies/admin/", AdminMovieApiView.as_view()),

    # movie sessions
    path("movie-sessions/", PrivateMovieSessionApiView.as_view()),

    # orders
    path("orders/", PrivateOrderApiView.as_view()),
]
