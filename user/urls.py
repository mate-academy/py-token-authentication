from django.urls import path

from user.views import UserCreate, UserLogin, UserManage


app_name = "user"

urlpatterns = [
    path("register/", UserCreate.as_view(), name="create"),
    path("login/", UserLogin.as_view(), name="login"),
    path("me/", UserManage.as_view(), name="manage")
]
