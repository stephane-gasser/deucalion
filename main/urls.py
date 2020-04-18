from django.conf.urls.defaults import *
from django.conf import settings
from views import default
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from filebrowser.sites import site as filebrowser_site
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'main.views.default'),                       
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/filebrowser/', filebrowser_site.urls),
    url(r'^profiles/', include('main.Profiles.urls')),
    url(r'^messages/', include('main.Messages.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^', include('main.Content.urls')),
)
if settings.SERVE_MEDIA:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)',  'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
    urlpatterns += staticfiles_urlpatterns()
