from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from user.views import MeView, RegisterView

app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="create"),
    path("me/", MeView.as_view(), name="manage"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
]
