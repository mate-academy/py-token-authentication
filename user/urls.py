from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from user.views import UserCreateView, MeView


router = DefaultRouter()

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", views.obtain_auth_token, name="login"),
    path("me/", MeView.as_view(), name="manage")
]

app_name = "user"
