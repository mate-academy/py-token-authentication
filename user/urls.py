# user/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserMeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"), # Aspas duplas
    path("login/", LoginView.as_view(), name="login"),       # Aspas duplas
    path("me/", UserMeView.as_view(), name="me"),             # Aspas duplas
]
