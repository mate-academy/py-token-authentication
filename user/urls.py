from django.urls import path

from user.views import UserCreateView, UserLoginView, UserRetrieveUpdateView


app_name = "user"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("me/", UserRetrieveUpdateView.as_view(), name="manage"),
    path("login/", UserLoginView.as_view(), name="login"),
]
