from django.urls import path
from rest_framework.authtoken import views

from user.views import (
    UserCreateAPIView,
    LoginUserAPIView,
    ManageUserAPIView
)


app_name = "user"


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="create"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path("me/", ManageUserAPIView.as_view(), name="manage"),
]
