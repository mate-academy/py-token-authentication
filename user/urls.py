# write your code here
from user.views import (CreateUserView,
                        LoginTokenView,
                        ManageUserView)
from django.urls import path, include


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage")
]

app_name = "user"
