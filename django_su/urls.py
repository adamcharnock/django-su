# -*- coding: utf-8 -*-

try:
    from django.conf.urls import url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import url

from .views import su_logout, su_login, login_as_user

urlpatterns = [
    url(r"^$", su_logout, name="su_logout"),
    url(r"^login/$", su_login, name="su_login"),
    url(r"^(?P<user_id>-?[\d]+)/$", login_as_user, name="login_as_user"),
]
