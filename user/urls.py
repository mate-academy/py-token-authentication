# write your code here
from user.views import CreateTokenView, UserView, CreateUserView
from django.urls import path

app_name = "user"


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", UserView.as_view(), name="manage"),
]
