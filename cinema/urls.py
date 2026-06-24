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


class RestrictedRouter(routers.DefaultRouter):
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        if getattr(viewset, "no_detail_route", False):
            detail_actions = {
                "retrieve",
                "update",
                "partial_update",
                "destroy"
            }
            routes = [
                route for route in routes
                if not any(
                    action in detail_actions
                    for action in route.mapping.values()
                )
            ]
        return routes


router = RestrictedRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("cinema_halls", CinemaHallViewSet)
router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "cinema"
