from django.urls import path
from rest_framework.authtoken import views
from user.views import CreateUserView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", views.obtain_auth_token, name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
