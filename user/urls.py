from django.urls import path
from .views import CreateUserView, LoginUserView, ManageUserView


app_name = "user"

urlpatterns = [
    path("refister/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
