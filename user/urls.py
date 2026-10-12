from django.urls import path

from user.views import RegisterUserView, LoginWithTokenView, ManagePersonalInfo

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="create"),
    path("login/", LoginWithTokenView.as_view(), name="login"),
    path("me/", ManagePersonalInfo.as_view(), name="manage"),
]

app_name = "user"
