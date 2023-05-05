from django.urls import path, include
from rest_framework import routers

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    MovieSessionViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()

router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("genres/", GenreViewSet.as_view(), name="genre-list"),
    path("actors/", ActorViewSet.as_view(), name="actor-list"),
    path("cinema_halls/", CinemaHallViewSet.as_view(), name="cinemahall-list"),
] + router.urls

app_name = "cinema"
