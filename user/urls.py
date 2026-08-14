from django.urls import path

from user.views import CreateUserView, LoginUserClass, MangeUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserClass.as_view(), name="login"),
    path("me/", MangeUserView.as_view(), name="manage"),
]
