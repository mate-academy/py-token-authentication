from django.urls import path
from .views import RegisterView, CustomAuthToken, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="create"),
    path("login/", CustomAuthToken.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
