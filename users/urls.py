from django.urls import path, include
from users.views import SignUpView, login_view, manage_users, user_info

app_name = "users"

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", login_view, name="login"),
    path("manage-users/", manage_users, name="manage_users"),
    path("user-info/", user_info, name="user-info")
]
