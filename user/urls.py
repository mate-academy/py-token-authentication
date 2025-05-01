from django.urls import path

from user.views import CreateUserAPIView, LoginUserView, ManageUserView

app_name = "user"
urlpatterns = [
    path("register/", CreateUserAPIView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
