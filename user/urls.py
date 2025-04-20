from django.urls import path, include
from rest_framework import routers

from user.views import (
    CreateUserView,
    LoginUserView,
    ManageUserView,
    UserListView
)

app_name = "user"

router = routers.DefaultRouter()
router.register("list", UserListView, basename="list")
urlpatterns = [
    path("", include(router.urls)),
    path("create/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
