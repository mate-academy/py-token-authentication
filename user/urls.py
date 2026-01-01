from django.urls import path

from user.views import (
    UserCreateView,
    UserDetailView,
    CreateTokenView
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", UserDetailView.as_view(), name="manage"),
]

app_name = "user"
