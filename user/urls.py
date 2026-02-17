from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="create"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("me/", views.ManageUserView.as_view(), name="manage"),
]
