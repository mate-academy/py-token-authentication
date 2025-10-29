from django.urls import include, path
from rest_framework import routers

from cinema.views import (
    ActorViewSet,
    CinemaHallViewSet,
    GenreViewSet,
    MovieSessionViewSet,
    MovieViewSet,
    OrderViewSet,
)

app_name = "cinema"

router = routers.DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("actors", ActorViewSet, basename="actor")
router.register("cinemahalls", CinemaHallViewSet, basename="cinemahall")
router.register("movies", MovieViewSet, basename="movie")
router.register("moviesessions", MovieSessionViewSet, basename="moviesession")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
