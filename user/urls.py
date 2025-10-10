# write your code here
from django.urls import path

from .views import AuthUserViewSet, ManageUserViewSet, CreateUserView

app_name = "user"

urlpatterns = [
    path("login/", AuthUserViewSet.as_view(), name="login_token"),
    path("me/", ManageUserViewSet.as_view(), name="me"),
    path("register/", CreateUserView.as_view(), name="register"),
]
