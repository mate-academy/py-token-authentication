from django.urls import path
from user.views import UserList, UserLogin, ManageUserView

urlpatterns = [
    path("register/", UserList.as_view(), name="create"),
    path("login/", UserLogin.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
