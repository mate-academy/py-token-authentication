from django.urls import path

from user import views

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="create"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("me/", views.ManageUserView.as_view(), name="manage"),
]

app_name = "user"
