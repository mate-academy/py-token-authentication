from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter, Route

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    MovieSessionViewSet,
    OrderViewSet,
)


class ListCreateRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list", "post": "create"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        )
    ]


class ListCreateRetrieveRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list", "post": "create"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={"get": "retrieve"},
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
    ]


list_create_router = ListCreateRouter()
list_create_router.register("genres", GenreViewSet)
list_create_router.register("actors", ActorViewSet)
list_create_router.register("cinema_halls", CinemaHallViewSet)
list_create_router.register("orders", OrderViewSet)

list_create_retrieve_router = ListCreateRetrieveRouter()
list_create_retrieve_router.register("movies", MovieViewSet)

full_router = DefaultRouter()
full_router.register("movie_sessions", MovieSessionViewSet)

urlpatterns = [
    path("", include(list_create_router.urls)),
    path("", include(list_create_retrieve_router.urls)),
    path("", include(full_router.urls)),
]

app_name = "cinema"
