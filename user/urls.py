from django.urls import path

from user.views import UserCreateView, UserDetailView, LoginTokenView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", LoginTokenView.as_view(), name="login"),
    path("me/", UserDetailView.as_view(), name="manage"),
]

app_name = "user"
