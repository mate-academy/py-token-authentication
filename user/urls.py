from django.urls import path, include
from rest_framework.authtoken import views

from user.views import CreateTokenView, CreateUserView, RetrieveUpdateView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", RetrieveUpdateView.as_view(), name="manage")
]


app_name = "user"
