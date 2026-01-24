# user/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserMeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", UserMeView.as_view(), name="me"),
]
