from django.urls import path

from user.views import UserRegisterViewSet, LoginUserView, ManagerUserView

app_name = "user"

urlpatterns = [
    path("register/", UserRegisterViewSet.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManagerUserView.as_view(), name="manage"),
]
