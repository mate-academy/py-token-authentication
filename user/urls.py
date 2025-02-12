from django.urls import path

from user.views import UserCreateView


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
]

app_name = "user"
