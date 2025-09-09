from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.views import CreateUserView, ManageUserView

app_name = "user"
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path(
        "login/",
        ObtainAuthToken.as_view(
            renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
        ),
        name="login"
    ),
    path("me/", ManageUserView.as_view(), name="manage")
]
