from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.views import CreateUserApiView, MeApiView


app_name = "user"

urlpatterns = [
    path("register/", CreateUserApiView.as_view(), name="create"),
    path("login/", obtain_auth_token, name="login"),
    path("me/", MeApiView.as_view(), name="manage"),
]
