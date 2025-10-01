from django.urls import path

from user.views import CreateUserView, LoginUserView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="get_token"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
]

app_name = "user"
