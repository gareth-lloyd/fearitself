from django.conf.urls.defaults import *
import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^fear/', include('fearitself.stories.urls')),
)
# serve static assets using the django's inbuilt method if in debug
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/glloyd/projects/rewired_state/fearitself/assets'}),
    )  
