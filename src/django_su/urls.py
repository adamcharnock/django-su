from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("django_su.views",
    url(r"^su/(?P<user_id>[\d]+)/$", "login_as_user", name="login_as_user"),
    url(r"^su/$", "su_exit", name="su_exit"),
)
