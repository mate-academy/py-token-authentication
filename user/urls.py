from django.urls import path

from user.views import UserRegisterView, UserObtainTokenView, UserMeView


app_name = "user"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="create"),
    path("login/", UserObtainTokenView.as_view(), name="login"),
    path("me/", UserMeView.as_view(), name="manage"),
]
