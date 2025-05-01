from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import LoginView, RegisterView, UserProfileView

app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="create"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", UserProfileView.as_view(), name="me"),
]
