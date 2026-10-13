from django.urls import path
from user.views import CreateUserView, ManageUserView
from rest_framework.authtoken.views import obtain_auth_token

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", obtain_auth_token, name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
