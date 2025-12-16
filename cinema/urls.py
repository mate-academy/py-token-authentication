from django.urls import path, include
from rest_framework import routers

from cinema.views import (
    GenreView,
    ActorView,
    CinemaHallView,
    MovieView,
    MovieSessionViewSet,
    OrderView,
)

router = routers.DefaultRouter()
router.register("movie_sessions", MovieSessionViewSet)

urlpatterns = [
    path("genres/", GenreView.as_view(), name="genre-list"),
    path("cinema_halls/", CinemaHallView.as_view(), name="cinemahall-list"),
    path("actors/", ActorView.as_view(), name="actor-list"),
    path(
        "movies/",
        MovieView.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="movie-list",
    ),
    path(
        "movies/<int:pk>/",
        MovieView.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="movie-detail",
    ),
    path(
        "orders/",
        OrderView.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="order-list",
    ),
    path("", include(router.urls)),
]

app_name = "cinema"
