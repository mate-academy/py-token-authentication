from django.urls import path
from .views import (
    CreateUserView,
    LoginUserView,
    ManageUserView
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="me"),
]

app_name = 'user'
