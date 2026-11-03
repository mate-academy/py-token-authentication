# write your code here
from django.urls import path

from user.views import LoginUserView, ManageUserView, CreateUserView

app_name = "user"


urlpatterns = [
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("register/", CreateUserView.as_view(), name="create"),
]
