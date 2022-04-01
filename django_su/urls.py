# -*- coding: utf-8 -*-

from django.urls import path

from .views import login_as_user, su_login, su_logout


urlpatterns = [
    path("", su_logout, name="su_logout"),
    path("login/", su_login, name="su_login"),
    path("<int:user_id>/", login_as_user, name="login_as_user"),
]
