from django.urls import path
from .views import UserRegisterView, UserLoginView, UserMeView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="create"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", UserMeView.as_view(), name="manage"),
]

app_name = "user"
