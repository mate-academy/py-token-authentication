from django.urls import path

from user.views import UserCreateView, UserTokenCreateView


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserTokenCreateView.as_view(), name="login_token")
]

app_name = "user"
