from django.urls import path
from .views import CreateUserView, LoginUserView, ManageUserView


app_name = "user"


urlpatterns = [
    path("login/", LoginUserView.as_view(), name="get_token"),
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
]
