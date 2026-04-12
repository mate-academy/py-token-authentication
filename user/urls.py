from django.contrib.auth.views import LoginView
from django.urls import path
from rest_framework.authtoken import views

from user.views import CreateUserView, CreateTokenView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="get_token"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
]
