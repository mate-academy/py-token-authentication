from django.urls import path

from user.views import UserRegisterView, UserTokenView, UserUpdateView

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="create"),
    path("login", UserTokenView.as_view(), name="login"),
    path("me", UserUpdateView.as_view(), name="manage"),
]

app_name = "user"
