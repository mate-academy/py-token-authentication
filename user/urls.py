from django.urls import path

from user.views import CreateUserView, CreateTokenView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
]

app_name = "user"
