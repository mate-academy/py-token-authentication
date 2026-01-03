from django.urls import path

from user.views import UserView, CreateTokenView, ManageUserView

urlpatterns = [
    path("register/", UserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
