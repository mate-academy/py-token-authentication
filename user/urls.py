from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from user.views import ProfileView, RegisterView

app_name = "user"

urlpatterns = [
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("me/", ProfileView.as_view(), name="manage"),
    path("register/", RegisterView.as_view(), name="create"),
]
