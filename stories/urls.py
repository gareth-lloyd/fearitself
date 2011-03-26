from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.fear),
    (r'^sources/$', views.sources),
    (r'^sources/(?P<source_id>\d+/init', views.initsource),
)
