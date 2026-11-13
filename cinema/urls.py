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
from user.views import (UserRegistrationView,
                        UserLoginView,
                        UserMeView
                        )


router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("cinema_halls", CinemaHallViewSet)
router.register("movies", MovieViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("user/register/", UserRegistrationView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    path("user/me/", UserMeView.as_view()),
    path("", include(router.urls))
]

app_name = "cinema"
