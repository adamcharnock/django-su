from django.conf.urls.defaults import *

from django_su.views import login_as_user, su_exit

urlpatterns = patterns("",
    url(r"^su/(?P<user_id>[\d]+)/$", login_as_user, name="login_as_user"),
    url(r"^su/$", su_exit, name="su_exit"),
)