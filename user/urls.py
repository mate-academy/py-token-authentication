from django.urls import path

from .views import (
    UserCreateView,
    UserLoginView, ManageUserView,
)


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]


app_name = "user"

