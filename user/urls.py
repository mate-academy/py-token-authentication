from django.urls import path

from .views import CreateUserView, LoginUserClass, ManageUserView
from rest_framework.authtoken import views

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserClass.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
