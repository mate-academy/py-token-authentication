from django.urls import path

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    MovieSessionViewSet,
    OrderViewSet,
)


genre_list = GenreViewSet.as_view(actions={
    "get": "list",
    "post": "create",
})
cinema_hall_list = CinemaHallViewSet.as_view(actions={
    "get": "list",
    "post": "create",
})
actor_list = ActorViewSet.as_view(actions={
    "get": "list",
    "post": "create",
})
movie_list = MovieViewSet.as_view(actions={
    "get": "list",
    "post": "create",
})
movie_detail = MovieViewSet.as_view(actions={
    "get": "retrieve",
})
movie_session_list = MovieSessionViewSet.as_view(actions={
    "get": "list",
    "post": "create",
})
movie_session_detail = MovieSessionViewSet.as_view(actions={
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})
order_list = OrderViewSet.as_view(actions={
    "get": "list",
    "post": "create",
})

urlpatterns = [
    path("genres/", genre_list, name="genre-list"),
    path("cinema_halls/", cinema_hall_list, name="cinemahall-list"),
    path("actors/", actor_list, name="actor-list"),
    path("movies/", movie_list, name="movie-list"),
    path("movies/<int:pk>/", movie_detail, name="movie-detail"),
    path("movie_sessions/", movie_session_list, name="moviesession-list"),
    path(
        "movie_sessions/<int:pk>/",
        movie_session_detail,
        name="moviesession-detail"
    ),
    path("orders/", order_list, name="order-list"),

]

app_name = "cinema"
