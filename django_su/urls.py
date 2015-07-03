# -*- coding: utf-8 -*-

try:
    from django.conf.urls import patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("django_su.views",
    url(r"^$", "su_logout", name="su_logout"),
    url(r"^login/$", "su_login", name="su_login"),
    url(r"^(?P<user_id>-?[\d]+)/$", "login_as_user", name="login_as_user"),
)
