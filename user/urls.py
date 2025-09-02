from django.urls import path
from .views import RegisterView, LoginView, MeView

app_name = "user"

urlpatterns = [
    # реєстрація
    path("register/", RegisterView.as_view(), name="register"),
    path("create/", RegisterView.as_view(), name="create"),

    # отримання токена
    path("login/", LoginView.as_view(), name="login"),
    path("token/", LoginView.as_view(), name="token"),

    # профіль користувача
    path("me/", MeView.as_view(), name="me"),
    path("manage/", MeView.as_view(), name="manage"),
]
