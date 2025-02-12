from django.urls import path
from user.views import ManageUserView, UserRegisterView, CreateTokenView


app_name = "user"

urlpatterns = [
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("create/", UserRegisterView.as_view(), name="create"),
]
