from django.urls import path
from .views import RegisterUserView, LoginUserView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
