from django.urls import path
from .views import UserViewSet, CreateTokenView

app_name = "user"

user_register = UserViewSet.as_view({"post": "create"})
user_me = UserViewSet.as_view({
    "get": "me",
    "put": "me",
    "patch": "me"
})

urlpatterns = [
    path("register/", user_register, name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", user_me, name="manage"),
]