from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

from ajax_select import urls as ajax_select_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^su/', include('django_su.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),                       
)
