from django.urls import path

from user.views import UserCreateAPIView, UserLoginAPIView, UserDetailAPIView

app_name = "user"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="create"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("me/", UserDetailAPIView.as_view(), name="me"),
]
