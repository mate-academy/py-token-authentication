from django.urls import path
from .views import LoginView, ManageUserView, RegisterView


app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="create"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
