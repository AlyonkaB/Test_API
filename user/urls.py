from django.urls import path

from user.views import CreateUserView, LoginUserClass, ManagerUserView
from rest_framework.authtoken import views


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user"),
    path('api-token-auth/', LoginUserClass.as_view(), name="get_token"),
    path('me/', ManagerUserView.as_view(), name="manage_user")
]

app_name = "user"
