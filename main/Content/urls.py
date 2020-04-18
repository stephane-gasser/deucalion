from django.conf.urls.defaults import *
from django.conf import settings

from main.Content.views import ContentIndexView, ContentPageView

urlpatterns = patterns(
    '',
    url('^index/$', ContentIndexView.as_view(), name="Content_index"),
    url('^(?P<site_url>fr/.*)$', ContentPageView.as_view(), name="Content_page")
    )
