from django.urls import path
from rest_framework.authtoken import views
from user.views import CreateUserView, CreateTokenView, ManageUserView

urlpatterns = [
   path("register/", CreateUserView.as_view(), name="create"),
   path("login/", CreateTokenView.as_view(), name="token"),
   path("me/", ManageUserView.as_view(), name="manage")
]

app_name = "user"