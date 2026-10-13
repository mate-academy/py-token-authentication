from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet, CreateTokenView, UserUpdateViewSet

router = DefaultRouter()

router.register("me", UserUpdateViewSet, basename="me")

urlpatterns = router.urls

urlpatterns += [
    path(
        "register/",
        UserViewSet.as_view({"post": "create"}),
        name="create",
    ),
    path(
        "me/",
        UserUpdateViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
            }
        ),
        name="manage",
    ),
    path("login/", CreateTokenView.as_view(), name="login"),
]

app_name = "user"
