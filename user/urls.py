from django.urls import path

from user.views import CreateUserView, CreateTokenView, ManageUserView
from rest_framework.authtoken import views

app_name = "user"
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage")
]
