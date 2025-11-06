from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView

app_name = "user"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="create"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", UserProfileView.as_view(), name="manage"),
]
