from django.urls import path

from user.views import UserCreateView, UserLogin, UserDetail

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", UserLogin.as_view(), name="login"),
    path("me/", UserDetail.as_view(), name="manage"),

]
app_name = "user"
