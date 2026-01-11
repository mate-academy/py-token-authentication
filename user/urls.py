from django.urls import path


from .views import RegisterView, LoginView, MeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="create"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="manage"),
]

app_name = "user"
