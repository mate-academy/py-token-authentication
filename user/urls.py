from django.urls import include, path
from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="create"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("me/", views.ManageUserView.as_view(), name="manage"),
]
