from django.urls import path

from user.views import CreateUserViews, LoginView, ManageUserView


urlpatterns = [
    path("register/", CreateUserViews.as_view(), name="create"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
