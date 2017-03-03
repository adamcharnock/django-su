from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^su/', include('django_su.urls')),
]
