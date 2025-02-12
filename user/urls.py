from django.urls import path

from user.views import UserCreateView, UserTokenCreateView, UserRetrieveUpdateView


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserTokenCreateView.as_view(), name="login_token"),
    path("me/", UserRetrieveUpdateView.as_view(), name="me"),
]

app_name = "user"
