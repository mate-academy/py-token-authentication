from django.urls import path

from user.views import UserRegisterView, UserLoginView, UserDetailView


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="create"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", UserDetailView.as_view(), name="manage"),
]

app_name = "user"
