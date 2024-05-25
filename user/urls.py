from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, LoginUserClass, ManagerUserView
from rest_framework.authtoken import views


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user"),
    # path('api-token-auth/', LoginUserClass.as_view(), name="get_token"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManagerUserView.as_view(), name="manage_user"),
]

app_name = "user"
