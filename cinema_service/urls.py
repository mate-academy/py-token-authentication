from rest_framework import routers
from django.urls import path, include

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    MovieSessionViewSet,
    OrderViewSet,
)


class RestrictedRouter(routers.DefaultRouter):
    def get_default_base_name(self, viewset):
        routes = super().get_routes(viewset)
        if getattr(viewset, "no_detail_route", False):
            detail_actions = {
                "retrieve",
                "update",
                "partial_update",
                "destroy",
            }
            routes = [
                route for route in routes if not any(
                    action in detail_actions for action in route.mapping.keys()
                )
            ]
        return viewset.__class__.__name__.lower()


router = RestrictedRouter()
router.register(r"genres", GenreViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"cinema-halls", CinemaHallViewSet)
router.register(r"movies", MovieViewSet)
router.register(r"movie-sessions", MovieSessionViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
