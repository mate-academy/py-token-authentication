from django.urls import path, include
from rest_framework import routers
from user.views import CreateUserView, LoginUserView, ManageUserView

app_name = "user"

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginUserView.as_view(), name="login"),
    path("register", CreateUserView.as_view(), name="register"),
    path("me", ManageUserView.as_view(), name="menage_user"),
]
