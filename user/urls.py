from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from user.views import ManageUserView, UserRegistrationView

app_name = "user"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="create"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
