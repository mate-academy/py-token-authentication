from django.urls import path
from . import views


app_name = "user"

urlpatterns = [
    path("register/", views.CreateUserView.as_view, name="register"),
    path("login/", views.CreateTokenView.as_view, name="token"),
    path("me/", views.ManageUserView.as_view, name="me")
]

