from django.urls import path
from rest_framework.authtoken import views
from rest_framework.views import APIView

from user.views import CreateUserView, ManageUserView, LoginUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage")
]
