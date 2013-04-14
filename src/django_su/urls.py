from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("django_su.views",
    url(r"^$", "su_exit", name="su_exit"),
    url(r"^login/$", "su_login", name="su_login"),
    url(r"^logout/$", "su_logout", name="su_logout"),
    url(r"^(?P<user_id>[\d]+)/$", "login_as_user", name="login_as_user"),
)
