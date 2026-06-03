from django.urls import path

from user.views import UserCreateAPIView, UserLoginAPIView


app_name = "user"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="create"),
    path("login/", UserLoginAPIView.as_view(), name="login")
]
