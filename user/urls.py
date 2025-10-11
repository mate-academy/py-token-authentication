from django.urls import path

from .views import AuthUserViewSet, ManageUserViewSet, CreateUserView

app_name = "user"

urlpatterns = [
    path("login/", AuthUserViewSet.as_view(), name="login"),
    path("me/", ManageUserViewSet.as_view(), name="manage"),
    path("register/", CreateUserView.as_view(), name="create"),
]
