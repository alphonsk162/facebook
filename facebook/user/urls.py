from django.urls import path
from .views import (
    login_page,
    signup_page,
    create_account,
    signin,
    signout,
    # trigger_export,
)

urlpatterns = [
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),
    path("create-account/", create_account, name="create_account"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    # path("export-users/", trigger_export, name="export_users"),
]
