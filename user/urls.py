from django.urls import path


from .views import CreateUserView, CreateTokenView, GetUpdateUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", GetUpdateUserView.as_view(), name="manage")
]

app_name = "user"
