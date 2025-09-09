from django.urls import path

from user.views import UserCreateView, UserLoginView, UserManageView


app_name = "user"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", UserManageView.as_view(), name="manage"),
]
