from django.urls import path

from user.views import (
    UserCreateView,
    TokenCreateView,
    UserManagingView
)

urlpatterns = [
    path(
        "register/", UserCreateView.as_view(), name="create"
    ),
    path(
        "login/", TokenCreateView.as_view(), name="login"
    ),
    path(
        "me/", UserManagingView.as_view(), name="manage"
    )
]

app_name = "user"
