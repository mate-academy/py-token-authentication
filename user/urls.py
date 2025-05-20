from django.urls import path
from .views import RegisterView, CustomAuthToken, ManageUserView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomAuthToken.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="me"),
]

