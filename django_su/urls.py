# -*- coding: utf-8 -*-

from django.urls import path

from .views import su_logout, su_login, login_as_user

urlpatterns = [
    path("", su_logout, name="su_logout"),
    path("login/", su_login, name="su_login"),
    path("<int:user_id>/", login_as_user, name="login_as_user"),
]
