from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("su/", include("django_su.urls")),
    path("", TemplateView.as_view(template_name="index.html")),
]

if "ajax_select" in settings.INSTALLED_APPS:
    from ajax_select import urls as ajax_select_urls

    urlpatterns += [
        path("admin/lookups/", include(ajax_select_urls)),
    ]
