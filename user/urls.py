from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.views import CreateUserView, MeUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", obtain_auth_token, name="login"),
    path("me/", MeUserView.as_view(), name="manage"),
]

app_name = "user"
