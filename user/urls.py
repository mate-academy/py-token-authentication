from django.urls import path
from user.views import RegisterView, LoginView, MeView

app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="create"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="manage"),
]
