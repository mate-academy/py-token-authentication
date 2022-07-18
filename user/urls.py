from django.urls import path

from user.views import UserCreateView, UserCreateTokenView, UserManageView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", UserCreateTokenView.as_view(), name="login"),
    path("me/", UserManageView.as_view(), name="manage"),
]

app_name = "user"
