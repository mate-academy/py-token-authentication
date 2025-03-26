from django.urls import path

from user.views import UserCreateView, ManageUserView, ObtainTokenView

app_name = "user"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", ObtainTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
