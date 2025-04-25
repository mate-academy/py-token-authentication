from django.urls import path, include
from rest_framework import routers

from cinema.views import (
    GenreListCreateView,
    ActorListCreateView,
    CinemaHallListCreateView,
    MovieListCreateView,
    MovieRetrieveView,
    MovieSessionListCreateView,
    MovieSessionRetrieveUpdateDestroyView, OrderListCreateView
)

urlpatterns = [
    path("genres/", GenreListCreateView.as_view(), name="genre-list"),
    path("actors/", ActorListCreateView.as_view(), name="actor-list"),
    path(
        "cinema_halls/",
        CinemaHallListCreateView.as_view(),
        name="cinemahall-list"
    ),
    path("movies/", MovieListCreateView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieRetrieveView.as_view(), name="movie-detail"),
    path(
        "movie_sessions/",
        MovieSessionListCreateView.as_view(),
        name="moviesession-list"
    ),
    path(
        "movie_sessions/<int:pk>/",
        MovieSessionRetrieveUpdateDestroyView.as_view(),
        name="moviesession-detail"
    ),
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
]

app_name = "cinema"
