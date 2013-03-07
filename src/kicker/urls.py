from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'kicker.views.kicker_view', name='kicker'),
    url(r'^admin/', include(admin.site.urls)),
)
