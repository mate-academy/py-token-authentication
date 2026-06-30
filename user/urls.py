from django.urls import path

from user.views import CreateUserView, CreateTokenView, UserMeView

app_name = "user"


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", UserMeView.as_view(), name="manage"),
]
