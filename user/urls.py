from django.urls import path

from user.views import (
    CreateUserView,
    ObtainAuthTokenView,
    UserRetrieveUpdateAPIView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", ObtainAuthTokenView.as_view(), name="login"),
    path("me/", UserRetrieveUpdateAPIView.as_view(), name="manage"),
]

app_name = "user"
