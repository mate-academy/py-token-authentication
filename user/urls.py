from django.urls import path

from user.views import CreateUserView, LoginUserView, ManagerUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManagerUserView.as_view(), name="manage")
]


app_name = "user"
