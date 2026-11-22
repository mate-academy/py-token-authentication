from django.urls import path
from .views import (
     CreateUserView,
     LoginUserView,
     ManageUserView
     )

app_name = "user"

urlpatterns = [
     path("register/", 
          CreateUserView.as_view(), name="register"),
     path("login/", 
          LoginUserView.as_view(), name="token-auth"),
     path("me/", 
          ManageUserView.as_view(), name="update")
]