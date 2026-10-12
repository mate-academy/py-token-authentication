
from rest_framework.authtoken import views
from django.urls import path
from .views import UserCreateView, UserManageView

app_name = "user"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", views.obtain_auth_token, name="login"),
    path("me/", UserManageView.as_view(), name="manage"),

]
