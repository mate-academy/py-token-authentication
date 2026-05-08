from django.urls import path
from rest_framework.authtoken import views

from user.views import CreateUserView, UserView

app_name = "user"
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", views.obtain_auth_token, name="login"),
    path("me/", UserView.as_view(), name="manage"),
]
