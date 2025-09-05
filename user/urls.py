from django.urls import path
from user.views import CreateUserView, LoginUserView, ManageUserViews

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserViews.as_view(), name="manage"),
]

app_name = "user"
