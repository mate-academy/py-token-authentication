# write your code here
from django.urls import path
from user.views import CreateUserViewSet, CreateTokenView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserViewSet.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
