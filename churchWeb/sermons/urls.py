from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from churchWeb.sermons.views import *

urlpatterns = patterns('sermons.views',
    # Examples:
    # url(r'^$', 'churchWeb.views.home', name='home'),
    # url(r'^churchWeb/', include('churchWeb.foo.urls')),
    (r'^$','main'),
    (r'^(?P<id>\d*)$','main'),
    (r'^login','login'),
    (r'^contents/(?P<id>\d*)','viewFolder'),
    (r'^editSermon/(?P<id>\d*)','editSermon'),
    (r'^editFolder/(?P<id>\d*)','editFolder'),
    (r'^editFolder$','editFolder'),
    (r'^editSermon$','editSermon'),
    (r'^delFolder/(?P<id>\d*)','deleteFolder'),
    (r'^delSermon/(?P<id>\d*)','deleteSermon'),
#    (r'^contents','viewFolder'),
#    (r'^editSermon','editSermon'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
