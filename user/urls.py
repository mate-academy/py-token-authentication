from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from user.views import CreateUserView, RetrieveUpdateUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", obtain_auth_token, name="login"),
    path("me/", RetrieveUpdateUserView.as_view(), name="manage"),
]
