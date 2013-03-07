from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('kicker.views',
    url(r'^$', 'kicker_view', name='kicker'),
    url(r'^admin/', include(admin.site.urls)),
) + patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', name='login'),
    url(r'^accounts/logout/$', 'logout', name='logout'),
)
