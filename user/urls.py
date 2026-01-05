from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="create"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("me/", views.UserMeView.as_view(), name="manage"),
]
